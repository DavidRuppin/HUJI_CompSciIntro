#################################################################
# FILE : math_print.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 ex1 2023
# WEB PAGES I USED: https://en.wikipedia.org/wiki/Golden_ratio
#################################################################

import math


def golden_ratio():
    print( (1 + 5 ** 0.5) / 2)


def six_squared():
    print(6 ** 2)


def hypotenuse():
    print((5 ** 2 + 12 ** 2) ** 0.5)


def pi():
    print(math.pi)


def e():
    print(math.e)


def squares_area():
    for width in range(1, 11):
        print(width * width, end="")
        if width < 10:
            print("", end=" ")
    print()

if __name__ == "__main__":
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
