# ----------------------------------------------------#
# FILE : ex3.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex3 2023 
# DESCRIPTION: A variety of different functions mostly dealing with lists
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES: Have a wonderful week <3
# ----------------------------------------------------#

def input_list():
    inputs = []
    input_sum = 0

    # My version of 'do while', while the user is entering non empty strings keep appending them to the list and
    # summing them in @input_sum
    user_input = input()
    while user_input != "":
        inputs.append(float(user_input))
        input_sum += inputs[-1]
        user_input = input()

    return inputs + [input_sum]


def inner_product(vec_1, vec_2):
    product = 0

    # Making sure the vectors are of similar size
    if len(vec_1) != len(vec_2):
        return None

    # Making sure the vectors are not empty
    if len(vec_1) == 0:
        return 0

    # Multiplying and summing the vectors
    for i in range(len(vec_1)):
        product += vec_1[i] * vec_2[i]

    return product


def sequence_monotonicity(sequence):
    if len(sequence) < 2:
        return [True, True, True, True]
    # Checking if the sequence is increasing and really increasing
    increasing = check_monotonicity_increasing(sequence)

    # Checking if the sequence is decreasing and really decreasing
    decreasing = check_monotonicity_increasing(sequence[::-1])

    # Returning the sum of both tests
    return increasing + decreasing


# Helper function to @sequence_monotonicity
def check_monotonicity_increasing(sequence):
    increasing, really_increasing = True, True

    # Iterating over the first n variables of @sequence, checking the monotonicity element by element
    for i in range(len(sequence) - 1):
        if sequence[i] > sequence[i + 1]:
            increasing, really_increasing = False, False
            break
        elif sequence[i] == sequence[i + 1]:
            really_increasing = False

    return [increasing, really_increasing]


def monotonicity_inverse(def_bool):
    # Created examples for every possible scenario
    examples = [[1, 2, 3, 4], [1, 2, 3, 3], [4, 3, 2, 1], [3, 2, 1, 1], [1, 1, 1, 1], [1, 0, 1, 0]]
    # Iterating over the examples, if one fits within @def_bool, return it
    for example in examples:
        if sequence_monotonicity(example) == def_bool:
            return example

    # If no example was found the definition is invalid, return None
    return None


def convolve(mat):
    if len(mat) == 0:
        return None

    new_mat = []

    for row in range(1, len(mat) - 1):
        # Creating a new result row
        new_mat.append([])
        for column in range(1, len(mat[0]) - 1):
            # Adding a new area value to the current result row
            new_mat[row - 1].append(square_area_around_point(row, column, mat))

    return new_mat


# Helper function to @convolve
def square_area_around_point(row, column, mat):
    area = 0
    # Getting the elements forming a 3x3 square with mat[row][column] as the center
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            area += mat[i][j]

    return area


def sum_of_vectors(vec_lst):
    if len(vec_lst) == 0 or len(vec_lst[0]) == 0:
        return None

    new_vec = []
    for index in range(len(vec_lst[0])):
        index_sum = 0
        for vector in vec_lst:
            index_sum += vector[index]

        new_vec.append(index_sum)

    return new_vec



def num_of_orthogonal(vectors):
    # Making sure vectors is non empty and that the inner vectors are not empty either
    if len(vectors) == 0 or len(vectors[0]) == 0:
        return 0

    result = 0
    # Iterating over all the vectors with the current vector becoming the starting point for the next iteration
    for i in range(len(vectors)):
        for j in range(i+1, len(vectors)):
            # If orthogonal add 1 to the result
            if inner_product(vectors[i], vectors[j]) == 0:
                result += 1

    return result
