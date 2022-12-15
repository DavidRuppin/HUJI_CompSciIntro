#################################################################
# FILE : lab8.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex8 2022-2023
#################################################################

import math
from typing import Set, List


def num_permutations(word):
    return 1 if len(word) == 0 else math.factorial(len(word))


def num_permutations_2(word):
    return 1 if len(word) <= 1 else len(word) * num_permutations(word[:-1])


def num_different_permutations(word):
    # The next line is here because this is how the tests check if your function is recursive:
    # they check if within any function there's a section that 'calls' recursively to the same function
    # by checking for the function's name and then a parenthesis, like this: 'func_name('
    # num_different_permutations(
    factorial = lambda n: 1 if n <= 1 else n * factorial(n - 1)

    n = factorial(len(word))
    sum = 1
    for char in set(word):
        sum *= factorial(word.count(char))

    return int(n / sum)


def factorial(n: int):
    return 1 if n <= 1 else n * factorial(n - 1)

def num_filtered_permutations(word):
