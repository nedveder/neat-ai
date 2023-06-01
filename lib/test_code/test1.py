import copy
import math
import sys
from typing import List
from PIL import Image
from copy import deepcopy

##############################################################################
#                                 CONSTANTS                                  #
##############################################################################
RED = 0.299
GREEN = 0.587
BLUE = 0.114
##############################################################################



##############################################################################
#                                 CONSTANTS                                  #
##############################################################################
GREYSCALE_CODE = "L"
RGB_CODE = "RGB"


##############################################################################
#                              Helper Functions                              #
##############################################################################
def load_image(image_filename):
    """
    Loads the image stored in the path image_filename and return it as a list
    of lists.
    :param image_filename: a path to an image file. If path doesn't exist an
    exception will be thrown.
    :return: a multi-dimensional list representing the image in the format
    rows X cols X channels. The list is 2D in case of a grayscale image and 3D
    in case it's colored.
    """
    img = Image.open(image_filename).convert('RGB')
    image = lists_from_pil_image(img)
    return image


def show_image(image):
    """
    Displays an image.
    :param image: an image represented as a multi-dimensional list of the
    format rows X cols X channels.
    """
    pil_image_from_lists(image).show()


def save_image(image, filename):
    """
    Converts an image represented as lists to an Image object and saves it as
    an image file at the path specified by filename.
    :param image: an image represented as a multi-dimensional list.
    :param filename: a path in which to save the image file. If the path is
    incorrect, an exception will be thrown.
    """
    pil_image_from_lists(image).save(filename)


def lists_from_pil_image(image):
    """
    Converts an Image object to an image represented as lists.
    :param image: a PIL Image object
    :return: the same image represented as multi-dimensional list.
    """
    width, height = image.size
    pixels = list(image.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    if type(pixels[0][0]) == tuple:
        for i in range(height):
            for j in range(width):
                pixels[i][j] = list(pixels[i][j])
    return pixels


def pil_image_from_lists(image_as_lists):
    """
    Creates an Image object out of an image represented as lists.
    :param image_as_lists: an image represented as multi-dimensional list.
    :return: the same image as a PIL Image object.
    """
    image_as_lists_copy = deepcopy(image_as_lists)
    height = len(image_as_lists_copy)
    width = len(image_as_lists_copy[0])

    if type(image_as_lists_copy[0][0]) == list:
        for i in range(height):
            for j in range(width):
                image_as_lists_copy[i][j] = tuple(image_as_lists_copy[i][j])
        im = Image.new(RGB_CODE, (width, height))
    else:
        im = Image.new(GREYSCALE_CODE, (width, height))

    for i in range(width):
        for j in range(height):
            im.putpixel((i, j), image_as_lists_copy[j][i])
    return im


def create_2D_list(rows: int, columns: int, value=0) -> List[List]:
    """
    :param rows: number of rows in new list
    :param columns: number of columns in new list
    :param value: value for cell
    :return: a 2D list
    """
    return [[value for _ in range(columns)] for __ in range(rows)]


def separate_channels(image: List[List[List[int]]]) -> List[List[List[int]]]:
    """
    :param image: Colored Image, 3D nested list
    :return: 3D nested list, separate color Channels
    """
    # Creates a empty 3D nested list
    channel_separation: List[List[List[int]]] = [[[] for _ in image] for __ in
                                                 image[0][0]]
    for c, channel in enumerate(channel_separation):
        for i, row in enumerate(image):
            for j, column in enumerate(row):
                channel[i].append(image[i][j][c])
    return channel_separation


def combine_channels(channels: List[List[List[int]]]) -> List[List[List[int]]]:
    """
    :param channels: 3D nested list, separate color Channels
    :return: Colored Image, 3D nested list
    """
    # Creates a empty 3D nested list
    channel_combination: List[List[List[int]]] = [[[] for _ in __]
                                                  for __ in channels[0]]
    for c, channel in enumerate(channels):
        for i, row in enumerate(channel):
            for j, column in enumerate(row):
                channel_combination[i][j].append(channel[i][j])
    return channel_combination


def RGB2grayscale(colored_image: List[List[List[int]]]) -> List[List[int]]:
    """
    :param colored_image: Colored Image, 3D nested list
    :return: Grayscale image 2D nested list
    """
    # Creates a 2D nested list where each value is
    # translated using RGB_pixel_to_grayscale function.
    new_image = [[RGB_pixel_to_grayscale(pixel) for pixel in row] for row in
                 colored_image]
    return new_image


def RGB_pixel_to_grayscale(pixel: List[int]) -> int:
    """
    :param pixel: Color value
    :return: Grayscale pixel value using color CONSTANTS
    """
    return int(round(pixel[0] * RED + pixel[1] * GREEN + pixel[2] * BLUE))


def blur_kernel(size: int) -> List[List[float]]:
    """
    Creates a Blur kernel SIZE*SIZE and 1 / (size ** 2) value in each cell
    :param size: Size of blur kernel
    """
    return create_2D_list(int(abs(size)),
                          int(abs(size)), 1 / size ** 2)


def apply_kernel_helper(image: List[List[int]], kernel: List[List[float]],
                        i: int, j: int) -> int:
    """
    Applies kernel to a specific pixel in the image using neighborhood_block
        function.
    """
    new_pixel = int(round(sum(neighborhood_block(image, len(kernel), i, j, True, kernel))))
    if new_pixel > 255:
        return 255
    elif new_pixel < 0:
        return 0
    else:
        return new_pixel


def apply_kernel(image: List[List[int]], kernel: List[List[float]]) \
        -> List[List[int]]:
    """
    Applies kernel to image using apply_kernel_helper function.
    Returns new image.
    """
    new_image = create_2D_list(len(image), len(image[0]))
    for i in range(len(image)):
        for j in range(len(image[0])):
            new_image[i][j] = apply_kernel_helper(image, kernel, i, j)
    return new_image


def bilinear_interpolation(image: List[List[int]], y: float, x: float) -> int:
    """
    The function applies bilinear interpolation formula to get the value of
    the pixel in a certin location after resizing the image, uses a weighted
    average of pixels around the wanted pixel
    """
    # Location of pixel
    normal_x, normal_y, = int(abs(x) // 1), int(abs(y) // 1)
    # Location inside the pixel
    frac_x, frac_y = abs(x) % 1, abs(y) % 1
    # Checks whether pixel is on image border/edge
    edge_y = 1 if len(image) > normal_y + 1 else 0
    edge_x = 1 if len(image[0]) > normal_x + 1 else 0
    a = image[normal_y][normal_x] * (1 - frac_x) * (1 - frac_y)
    b = image[normal_y + edge_y][normal_x] * (1 - frac_x) * frac_y
    c = image[normal_y][normal_x + edge_x] * frac_x * (1 - frac_y)
    d = image[normal_y + edge_y][normal_x + edge_x] * frac_x * frac_y
    weighted_average = int(round(a + b + c + d))
    return weighted_average


def resize(image: List[List[int]], new_height: int, new_width: int) \
        -> List[List[int]]:
    """
    :param image: 2D List(single channel or grayscale)
    :param new_height: height of outputted new image
    :param new_width: width of outputted new image
    :return: New resized image
    """
    new_image = [[0 for _ in range(new_width)] for __ in range(new_height)]
    resize_height_ratio = len(image) / new_height
    resize_width_ratio = len(image[0]) / new_width
    # Foreach pixel in new image sets value using bilinear_interpolation
    for y, row in enumerate(new_image):
        for x, column in enumerate(row):
            new_image[y][x] = bilinear_interpolation(image,
                                                     y * resize_height_ratio,
                                                     x * resize_width_ratio)
    # Sets corner pixels to be exact as the original image
    new_image[0][0] = image[0][0]
    new_image[new_height - 1][0] = image[len(image) - 1][0]
    new_image[0][new_width - 1] = image[0][len(image[0]) - 1]
    new_image[new_height - 1][new_width - 1] = image[len(image) - 1][
        len(image[0]) - 1]
    return new_image


def rotate_90(image: List[List], direction: str) -> List[List]:
    """
    Rotates the image 90 degrees in the direction inputted to the function.
    Returns new list.
    """
    # Creates a new 2D list, with flipped lengths
    new_image = create_2D_list(len(image[0]), len(image))
    if direction == "R":
        for j, column in enumerate(image[0]):
            for i, row in enumerate(image[::-1]):
                new_image[j][i] = copy.deepcopy(row[j])
    if direction == "L":
        for j, column in enumerate(image[0]):
            for i, row in enumerate(image):
                new_image[j][i] = copy.deepcopy(row[j])
        new_image = new_image[::-1]
    return new_image


def get_edges(image: List[List[int]], blur_size: int,
              block_size: int, c: int) -> List[List[int]]:
    """
    :param image: 2D nested list image (R/G/B or grayscale)
    :param blur_size: Blur parameter, for applying kernel
    :param block_size: Block size for edge detection
    :param c: Constant for edge detection
    :return: Returns a 2D image of edges (black on white background)
    """
    new_image = create_2D_list(len(image), len(image[0]), 255)
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    for i, row in enumerate(new_image):
        for j, column in enumerate(new_image[0]):
            # Sum of all pixels around i,j with radius depending on block_size
            neighborhood = neighborhood_block(blurred_image, block_size, i, j,
                                              True)
            # Average of the neighborhood
            threshold = int(round(sum(neighborhood) / len(neighborhood)))
            if blurred_image[i][j] < threshold - c:
                new_image[i][j] = 0
    return new_image


def neighborhood_block(image: List[List[int]], block_size: int, i: int,
                       j: int, with_edges: bool = False,
                       factor: List[List[float]] = None) -> List[float]:
    """
    Returns the factored sum of all values around i,j in image.
    with_edges adds the same image[i][j] to the block if no value exists.
    """
    radius = block_size // 2
    block = []
    if not factor:
        factor = create_2D_list(block_size + 1, block_size + 1, 1)
    for r in range(-radius, radius + 1):
        for s in range(-radius, radius + 1):
            if 0 <= i + r < len(image) and 0 <= j + s < len(image[0]):
                block.append(float(image[i + r][j + s] * factor[radius + r][radius + s]))
            elif with_edges:
                block.append(float(image[i][j] * factor[radius + r][radius + s]))
    return block


def quantize_pixel(pixel: int, N: int) -> int:
    """
    :param pixel: Color value of pixel
    :param N: Number of different colors to limit
    :return: Color value after using a normalizing formula
    """
    return int(round(math.floor(pixel * (N / 255)) * 255 / N))


def quantize(image: List[List[int]], N: int) -> List[List[int]]:
    """
    :param image: a 2D nested list image.
    :param N: number of colors to limit channel to.
    :return: returns a new layer after quantization.
        Uses quantize_pixel function
    """
    new_image = create_2D_list(len(image), len(image[0]))
    for i, row in enumerate(new_image):
        for j, column in enumerate(row):
            # Runs quantize_pixel for each pixel in the channel
            new_image[i][j] = quantize_pixel(image[i][j], N)
    return new_image


def quantize_colored_image(image: List[List[List[int]]], N: int) \
        -> List[List[List[int]]]:
    """
    :param image: an image to quantize
    :param N: limits number of colors in each channel
    :return: returns a new quantized image, uses quantize function.
    """
    rgb_image = separate_channels(image)
    new_rgb_image = []
    for channel in rgb_image:
        new_rgb_image.append(quantize(channel, N))
    return combine_channels(new_rgb_image)


def image_size(images: List) -> bool:
    """
    :param images: a list of images
    :return: returns True if all images are the same size, if not returns False
    """
    height = len(images[0])
    width = len(images[0][0])
    for image in images[1:]:
        if len(image) != height or len(image[0]) != width:
            return False
    return True


def add_mask(image1: List[List], image2: List[List], mask: List[List[int]]) \
        -> List[List]:
    """
    :param image1: An image 2D or 3D nested list
    :param image2: An image 2D or 3D nested list
    :param mask: A mask 2D nested list(can use create_mask function)
    :return: The function returns a new image after putting the two images one
        on the other using the mask. Makes use of add_mask_channel function.
    """
    # Checks if all images are the same size, if so runs the algo
    # else returns image1
    if image_size([image1, image2, mask]):
        # 4 different cases for combinations of 2D and 3D images.
        # Case 1: Both are 3D images
        image_1_list = type(image1[0][0]) == list
        image_2_list = type(image2[0][0]) == list
        if image_1_list and image_2_list:
            channels1 = separate_channels(image1)
            channels2 = separate_channels(image2)
            return combine_channels(
                [add_mask_channel(channels1[i], channels2[i], mask) for i in
                 range(len(channels1))])
        # Case 2: image1 is 2D image2 is 3D
        elif not image_1_list and image_2_list:
            channels2 = separate_channels(image2)
            return combine_channels(
                [add_mask_channel(image1, channels2[i], mask) for i in
                 range(len(channels2))])
        # Case 3: image1 is 3D image2 is 2D
        elif image_1_list and not image_2_list:
            channels1 = separate_channels(image1)
            return combine_channels(
                [add_mask_channel(channels1[i], image2, mask) for i in
                 range(len(channels1))])
        # Case 4: image1 is 2D image2 is 2D
        else:
            return add_mask_channel(image1, image2, mask)
    else:
        return image1


def add_mask_channel(image1: List[List[int]], image2: List[List[int]],
                     mask: List[List[int]]) \
        -> List[List[int]]:
    """
    The function adds a mask to a single channel image(R/G/B or grayscale)
    :return: a new 2D nested list
    """
    new_image = create_2D_list(len(image1), len(image1[0]))
    for i, row in enumerate(new_image):
        for j, column in enumerate(row):
            new_image[i][j] = int(round(image1[i][j] * mask[i][j] +
                                        image2[i][j] * (1 - mask[i][j])))
    return new_image


def create_mask(image: List[List[int]], height: int, width: int) -> List[
                    List[int]]:
    """
    :param image: image to create a mask from to
    :param height:height to adjust mask
    :param width:width to adjust mask
    :return: a mask that can be used to add to a color channel / image
    """
    resized_image = resize(image, height, width)
    return [[int(round(pixel / 255)) for pixel in row]
            for row in resized_image]


def cartoonify(image: List[List[List[int]]], blur_size: int,
               block_size: int, c_constant: int,
               quantize_num_shades: int) -> List[List[List[int]]]:
    """
    :param image: 3D nested list
    :param blur_size: used for get_edges function
    :param block_size: used for get_edges function
    :param c_constant: Used for get_edges function
    :param quantize_num_shades: used for quantize function
    :return: A cartoon image
    """
    grayscale_image = RGB2grayscale(image)
    image_edges = get_edges(grayscale_image, blur_size,
                            block_size, c_constant)
    quantized_image = quantize_colored_image(image, quantize_num_shades)
    mask = create_mask(image_edges, len(image), len(image[0]))
    cartooned_image = add_mask(quantized_image, mask, mask)
    return cartooned_image


def resize_with_ratio(image: List[List[List[int]]], max_size: int) -> \
        List[List[List[int]]]:
    """
    :param image: 3D nested List (multiple color channels)
    :param max_size: maximum size for image
    :return: New resized image with correct height X width ratio
    """
    height = len(image)
    width = len(image[0])
    ratio = height / width
    new_height = int(round(ratio * max_size))
    new_width = int(round(max_size))
    # image[0][0] is number of color channels
    new_image = combine_channels(
        [resize(separate_channels(image)[i], new_height, new_width)
         for i in range(len(image[0][0]))])
    return new_image


if __name__ == "__main__":
    if len(sys.argv) == 8:
        # Places args from terminal into variables
        image_source = sys.argv[1]
        cartoon_dest = sys.argv[2]
        max_im_size = int(sys.argv[3])
        blur_size_constant = int(sys.argv[4])
        th_block_size = int(sys.argv[5])
        th_c = int(sys.argv[6])
        quant_num_shades = int(sys.argv[7])
        # Manipulates the image, and outputs its to destination
        original_image = ex5_helper.load_image(image_source)
        resize_image = resize_with_ratio(original_image, max_im_size)
        cartoonify_image = cartoonify(resize_image, blur_size_constant,
                                      th_block_size, th_c, quant_num_shades)
        ex5_helper.save_image(cartoonify_image, cartoon_dest)
    else:
        print("Error, Please enter correct parameters.")
