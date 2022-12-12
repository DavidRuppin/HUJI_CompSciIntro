#################################################################
# FILE : ex7.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex7 2022-2023
# WEB PAGES I USED: https://en.wikipedia.org/wiki/Tower_of_Hanoi
#################################################################
from functools import lru_cache
from typing import Any, List

from ex7_helper import *


def mult(x: N, y: int) -> N:
    """Multiplies x by y recursively"""
    if x == 0 or y == 0:
        return 0

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

    if x == 0 or y == 0:
        return res

    if y > 1:
        res = log_mult(add(x, x), divide_by_2(y))

    if is_odd(y):
        res = add(res, x)

    return res


def is_power(b: int, x: int) -> bool:
    # 0 ^ 1 == 0
    if (b == 0 and x == 0) or x == 1:
        return True

    # Making sure both numbers aren't negative
    if b <= 0 or x <= 0:
        return False

    # If x is 1 then b ^ 0 == x
    if x == 1:
        return True

    # An even number times itself will never be odd and vice versa
    if is_odd(b) != is_odd(x) or (b == 1 and x != 1):
        return False

    return is_power_helper(b, x, b)


def is_power_helper(powered: int, x: int, original: int) -> bool:
    """Squaring powered until it exceeds x and then brute forcing the rest of the way"""
    if powered == x:
        return True

    new_powered = log_mult(powered, powered)

    if new_powered < x:
        return is_power_helper(new_powered, x, original)

    return is_power_helper_bruteforce(powered, x, original)


def is_power_helper_bruteforce(powered: int, x: int, original: int) -> bool:
    """Going @powered by @original until we either reached x or exceeded it and returning True or False appropriately"""
    if powered > x:
        return False
    if powered == x:
        return True
    return is_power_helper_bruteforce(log_mult(powered, original), x, original)


# def is_power(b: int, x: int) -> bool:
#     # 0 ^ 1 == 0
#     if b == 0 and x == 0 or x == 1:
#         return True
#
#     # Making sure both numbers aren't negative
#     if b <= 0 or x <= 0:
#         return False
#
#     # If x is 1 then b ^ 0 == x
#     if x == 1:
#         return True
#
#     # An even number times itself will never be odd and vice versa
#     if is_odd(b) != is_odd(x):
#         return False
#
#     return is_power_helper(b, x, b)
#
#
# def is_power_helper(b: int, x: int, powered: N) -> bool:
#     # Every number power zero is 1, if x == b then it's also a product of b power 1
#     if x == powered:
#         return True
#
#     # if b ^ n > x // 2 then b is too big
#     if powered > divide_by_2(x):
#         return False
#
#     next_powered: N = log_mult(powered, b)
#     if is_power_helper(b, x, next_powered):
#         return True
#
#     return False


def reverse(s: str) -> str:
    return reverse_helper(s)


def reverse_helper(s: str, flipped: str = '') -> str:
    if len(flipped) == len(s):
        return flipped
    return reverse_helper(s, append_to_end(flipped, s[len(s) - len(flipped) - 1]))


Tower = Any


def play_hanoi(hanoi: Any, number_of_discs: int, source: Tower, target: Tower, auxiliary: Tower) -> None:
    # As long as we have disks to move
    if number_of_discs > 0:
        play_hanoi(hanoi, number_of_discs - 1, source, auxiliary, target)

        hanoi.move(source, target)

        play_hanoi(hanoi, number_of_discs - 1, auxiliary, target, source)


def number_of_ones(n: int) -> int:
    if n == 0:
        return 0

    if n >= 19:
        initial_count = 0
        if n % 10 != 9:
            initial_count = one_count_in_num(n - (n % 10))
            initial_count *= (1 + (n % 10))
            if n % 10 >= 1:
                initial_count += 1
            n -= n % 10 + 1

        count = one_count_in_num(n - (n % 10))
        count *= (1 + (n % 10))
        count += 1 + initial_count

        return count + number_of_ones(n - 10)
    elif n < 10:
        return 1
    else:
        return one_count_in_num(n) + number_of_ones(n - 1)

def one_count_in_num(n: int) -> int:
    if n == 0:
        return 0

    res = 0

    if n % 10 == 1:
        res += 1

    return res + one_count_in_num(n // 10)


def compare_2d_lists(a: List[List[int]], b: List[List[int]]) -> bool:
    # If a and b aren't of the same size they can't be similar
    if len(a) != len(b):
        return False

    # If both lists are empty they're similar
    if len(a) == 0:
        return True

    return compare_2d_lists_helper(a, b)


def compare_2d_lists_helper(a: List[List[int]], b: List[List[int]], index: int = 0) -> bool:
    """Going sublist by sublist and checking the lists using the second helper function"""
    if index == len(a):
        return True

    if len(a[index]) != len(b[index]):
        return False

    return compare_2d_lists_helper(a, b, index + 1) and compare_same_sized_lists(a[index], b[index])


def compare_same_sized_lists(a: List[int], b: List[int], index: int = 0) -> bool:
    """This function compares two lists, object by object, recursively"""
    if index == len(a):
        return True

    return a[index] == b[index] and compare_same_sized_lists(a, b, index + 1)


def magic_list(n: int) -> List[Any]:
    if n == 0:
        return []

    previous_list = magic_list(n - 1)
    return [*previous_list, previous_list]
