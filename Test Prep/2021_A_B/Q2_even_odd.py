#################################################################
# FILE : Q2_even_odd.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest_2021_A_B 2022-2023
#################################################################

def even_odd(lst):
    return [i for i  in lst if i % 2 == 0] + [j for j in lst if j % 2 == 1]

def test_even_odd():
    assert even_odd([5, 4, -6, 9, 7]) == [4, -6, 5, 9, 7]


if __name__ == '__main__':
    test_even_odd()