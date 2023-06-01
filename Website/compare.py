def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1:
        content1 = file1.read()

    with open(file2_path, 'r') as file2:
        content2 = file2.read()

    # Compare the contents of the files
    if content1 == content2:
        return "Files are identical"
    else:
        return "Files are different"

if __name__ == '__main__':
    import sys

    # Get the file paths from command-line arguments
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    # Call the compare_files function
    result = compare_files(file1_path, file2_path)

    # Print the result
    print(result)
