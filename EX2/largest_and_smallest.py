# ----------------------------------------------------#
# FILE : largest_and_smallest.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex2 2023 
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES:
# ----------------------------------------------------#
from collections import namedtuple


def largest_and_smallest(a, b, c):
    largest, smallest = a, a
    for param in [a, b, c]:
        if param > largest:
            largest = param
        if param < smallest:
            smallest = param

    return largest, smallest


def check_largest_and_smallest():
    Test = namedtuple("Test", ["params", "answer"])
    tests = [Test((17, 1, 6), (17, 1)), Test((1, 17, 7), (17, 1)), Test((1, 1, 2), (2, 1)), Test((-1, -1, 0), (0, -1)),
             Test((0, 0, 0), (0, 0))]

    for test in tests:
        answer = largest_and_smallest(*test.params)
        if answer != test.answer:
            return False

    return True
