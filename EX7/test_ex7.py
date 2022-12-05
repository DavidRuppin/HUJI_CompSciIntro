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
    assert is_power(2, 4096) is True
    assert is_power(5, 1953123) is False
    assert is_power(5, 1953124) is False
    assert is_power(5, 1953125) is True
    assert is_power(5, 1953126) is False


def test_reverse():
     assert reverse('intro') == 'ortni'