#################################################################
# FILE : ex7.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex7 2022-2023
#################################################################

from ex7_helper import *


def mult(x: N, y: int) -> N:
    """Multiplies x by y recursively"""
    if y > 1:
        y = subtract_1(y)
        return add(mult(x, y), x)
    return x


def is_even(n: int) -> bool:  # type: ignore
    if n > 1:
        return is_even(subtract_1(subtract_1(n)))
    if n == 1:
        return False
    if n == 0:
        return True


def log_mult(x: N, y: int) -> N:
    res: N = 0

    if y > 1:
        res = log_mult(add(x, x), divide_by_2(y))

    if is_odd(y):
        res = add(res, x)

    return res


def is_power(b: int, x: int) -> bool:
    # Making sure both numbers aren't negative
    if b < 0 or x < 0:
        return False

    # If x is 1 then b ^ 0 == x
    if x == 1:
        return True

    # An even number times itself will never be odd and vice versa
    if is_odd(b) != is_odd(x):
        return False

    return is_power_helper(b, x, b)


def is_power_helper(b: int, x: int, powered: N) -> bool:
    # Every number power zero is 1, if x == b then it's also a product of b power 1
    if x == powered:
        return True

    # b is too big
    if powered > divide_by_2(x):
        return False

    powd: N = log_mult(powered, b)
    if is_power_helper(b, x, powd):
        return True

    return False


def reverse(s: str) -> str:
    return reverse_helper(s)


def reverse_helper(s: str, flipped: str = '') -> str:
    if len(flipped) == len(s):
        return flipped
    return reverse_helper(s, append_to_end(flipped, s[len(s) - len(flipped) - 1]))
