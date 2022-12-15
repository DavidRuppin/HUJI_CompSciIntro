#################################################################
# FILE : test_lab8.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex8 2022-2023
#################################################################

from lab8 import *


def test_num_permutations():
    assert num_permutations("ab") == 2
    assert num_permutations("abc") == 6
    assert num_permutations("abcd") == 24


def test_num_permutations_2():
    assert num_permutations_2("ab") == 2
    assert num_permutations_2("abc") == 6
    assert num_permutations_2("abcd") == 24


def test_num_different_permutations():
    assert num_different_permutations("abc") == 6
    assert num_different_permutations('abb') == 3
    assert num_different_permutations('') == 1

