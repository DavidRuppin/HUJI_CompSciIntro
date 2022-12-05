#################################################################
# FILE : lab7.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex7 2022-2023
#################################################################

from itertools import permutations as pms


def up_and_right(n, k, lst):
    moves = [*['r'] * n, *['u'] * k]

    pms(moves)


if __name__ == '__main__':
    lst = []
    up_and_right(10, 2, lst)
    lst.sort()
    for i in range(len(lst)):
        print(lst[i])
