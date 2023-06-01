def input_list():
    """
    :return: the function receives inputs from the user as long as the input
        isn't empty. adds all values to a list, calculates the sum of values
        and appends it to the list, the list is returned to the user.
    """
    input_string = input()
    if not input_string:
        return [0]
    inputs_list = []
    total_sum = 0
    while input_string:
        inputs_list.append(float(input_string))
        total_sum += float(input_string)
        input_string = input()
    inputs_list.append(total_sum)
    return inputs_list


def inner_product(vec_1, vec_2):
    """
    :param vec_1: vector - list of numbers
    :param vec_2: vector - list of numbers
    :return:the function returns the inner product multiplication of the two
        vectors.
    """
    if vec_1 or vec_2:
        if len(vec_1) == len(vec_2):
            product = 0
            for i in range(len(vec_1)):
                product += vec_1[i] * vec_2[i]
            return product
        return None
    else:
        return 0


def sequence_monotonicity(sequence):
    """
    :param sequence: a sequence of numbers
    :return:a list of 4 boolean values, upward or equal monotonicity,upward
        monotonicity,downward or equal monotonicity,downward monotonicity.
    """
    monotone_values = [True, True, True, True]
    if sequence and len(sequence) > 1:
        for i in range(len(sequence) - 1):
            diff = sequence[i] - sequence[i + 1]  #
            # Checks whether series is heading up or equal
            if diff <= 0:
                monotone_values[3] = False
                # Checks whether series is only heading up
                if diff < 0:
                    monotone_values[2] = False
            # Checks whether series is heading down or equal
            if diff >= 0:
                monotone_values[1] = False
                # Checks whether series is only heading down
                if diff > 0:
                    monotone_values[0] = False
    return monotone_values


def monotonicity_inverse(def_bool):
    """
    :param def_bool: list of 4 boolean values
    :return: the function returns a list of values that follow the rules from
        the boolean list [upward or equal monotonicity,upward
        monotonicity,downward or equal monotonicity,downward monotonicity]
    """
    # Checks for impossible cases
    if (def_bool[0] and def_bool[1] and def_bool[2] and def_bool[3]) or \
            (def_bool[1] and def_bool[2]) or (def_bool[0] and def_bool[3]):
        return None
    # Checks for equal series
    if def_bool[0] and def_bool[2]:
        return [1, 1, 1, 1]
    # Checks for random series (no restrictions)
    if not (def_bool[0] or def_bool[1] or def_bool[2] or def_bool[3]):
        return [1, 3, 2, 4]
    # Checks for upward monotonicity
    if def_bool[0]:
        if def_bool[1]:
            return [1, 2, 3, 4]
        return [1, 3, 3, 4]
    # Checks for downward monotonicity
    if def_bool[2]:
        if def_bool[3]:
            return [4, 3, 2, 1]
        return [4, 3, 3, 1]


def primes_for_asafi(n):
    """
    :param n: a number
    :return: returns a list of n primes in ordered list
    """
    if n == 0:
        return []
    prime_list = [2]
    number = 3
    while len(prime_list) < n:  # the loop runs until n primes in list
        for prime in prime_list:
            # if condition is met and still in loop the number is prime
            if prime ** 2 > number:
                prime_list.append(number)
                break
            # checks to see whether number has any other prime divisors
            if number % prime == 0:
                break
        number += 1
    return prime_list


def sum_of_vectors(vec_lst):
    """
    :param vec_lst: a list containing vectors of the same size
    :return: the function returns the sum of all vectors in inputted list
    """
    if vec_lst:
        vec_sum = [0]*len(vec_lst[0])
        for vector in vec_lst:
            if vector:
                for index in range(len(vector)):
                    vec_sum[index] += vector[index]
        return vec_sum
    return None


def num_of_orthogonal(vectors):
    """
    :param vectors: a list containing vectors of the same size
    :return: the function returns the number of vectors pairs which are
        perpendicular.
    """
    count = 0
    for i in range(len(vectors)):
        # the loop starts from i so it doesnt count twice
        for j in range(i, len(vectors)):
            if i != j:
                if inner_product(vectors[i], vectors[j]) == 0:
                    count += 1
    return count