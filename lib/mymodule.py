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