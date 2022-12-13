#################################################################
# FILE : lab7.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex7 2022-2023
#################################################################

from itertools import permutations as pms


def up_and_right(n, k, lst):
    moves = [*['r'] * n, *['u'] * k]

    pms(moves)


def number_of_ones(n):
    pass


def number_of_ones_helper(n, original):
    if original > n:
        return 0


def number_of_ones_bruteforce(n, original):
    if n <= original:
        return one_count_in_num(n) + number_of_ones_bruteforce(n + 1, original)


def one_count_in_num(n: int) -> int:
    if n == 0:
        return 0

    res = 0

    if n % 10 == 1:
        res += 1

    return res + one_count_in_num(n // 10)


if __name__ == '__main__':
    assert number_of_ones(0) == 0
    assert number_of_ones(1) == 1
    assert number_of_ones(2) == 1
    assert number_of_ones(3) == 1
    assert number_of_ones(4) == 1
    assert number_of_ones(5) == 1
    assert number_of_ones(6) == 1
    assert number_of_ones(7) == 1
    assert number_of_ones(8) == 1
    assert number_of_ones(10) == 2
    assert number_of_ones(11) == 4
    assert number_of_ones(13) == 6
    assert number_of_ones(20) == 12
    assert number_of_ones(99) == 20
    assert number_of_ones(100) == 21
    assert number_of_ones(101) == 23
    assert number_of_ones(109) == 31
    assert number_of_ones(110) == 33
    assert number_of_ones(131) == 66
    assert number_of_ones(177) == 116
    assert number_of_ones(276) == 158
    assert number_of_ones(941) == 295
    assert number_of_ones(553) == 216
    assert number_of_ones(311) == 164
    assert number_of_ones(950) == 295
    assert number_of_ones(4785) == 2459
    assert number_of_ones(9468) == 3897
    assert number_of_ones(168961) == 156659
    assert number_of_ones(157234123) == 187658381
