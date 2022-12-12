#################################################################
# FILE : test_ex7.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex7 2022-2023
#################################################################

from ex7 import *


def test_mult():
    assert mult(4, 3) == 12
    assert mult(500, 4) == 2000
    assert mult(1.5, 4) == 6


def test_is_even():
    assert is_even(900) is True
    assert is_even(1) is False


def test_log_mult():
    assert log_mult(4, 3) == 12
    assert log_mult(500, 4) == 2000
    assert log_mult(1.5, 4) == 6


def test_is_power():
    assert is_power(2, 16) is True
    assert is_power(2, 32) is True
    assert is_power(3, 17) is False
    assert is_power(1, 1) is True
    assert is_power(0, 1) is True
    assert is_power(1, 0) is False
    assert is_power(0, 2) is False
    assert is_power(2, 4096) is True
    assert is_power(5, 1953123) is False
    assert is_power(5, 1953124) is False
    assert is_power(5, 1953125) is True
    assert is_power(5, 1953126) is False


def test_reverse():
    assert reverse('intro') == 'ortni'
    assert reverse('h') == 'h'
    assert reverse('') == ''


def test_number_of_ones():
    assert number_of_ones(13) == 6
    assert number_of_ones(9) == 1
    assert number_of_ones(0) == 0
    assert number_of_ones(21) == 13


def test_compare_2d_lists():
    assert compare_2d_lists([[1, 2], [4, 5, 6]], [[1, 2], [4, 5, 8]]) is False
    assert compare_2d_lists([[1, 2, 3, 4], [5, 6, 7, 8, 9, 10], []], [[1, 2, 3, 4], [5, 6, 7, 8, 9, 10], []]) is True
    assert compare_2d_lists([], []) is True
    assert compare_2d_lists([[], []], [[], []]) is True
    assert compare_2d_lists([[], []], [[]]) is False


def test_magic_list():
    assert magic_list(0) == []
    assert magic_list(1) == [[]]
    assert magic_list(2) == [[], [[]]]
    assert magic_list(3) == [[], [[]], [[], [[]]]]
