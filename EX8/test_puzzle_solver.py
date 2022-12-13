#################################################################
# FILE : test_puzzle_solver.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex8 2022-2023
#################################################################

from puzzle_solver import *


def test_max_seen_cells():
    picture = [[-1, 0, 1, -1],
               [0, 1, -1, 1],
               [1, 0, 1, 0]]

    assert max_seen_cells(picture, 0, 0) == 1
    assert max_seen_cells(picture, 1, 0) == 0
    assert max_seen_cells(picture, 1, 2) == 5
    assert max_seen_cells(picture, 1, 1) == 3


def test_min_seen_cells():
    picture = [[-1, 0, 1, -1],
               [0, 1, -1, 1],
               [1, 0, 1, 0]]

    assert min_seen_cells(picture, 0, 0) == 0
    assert min_seen_cells(picture, 1, 0) == 0
    assert min_seen_cells(picture, 1, 2) == 0
    assert min_seen_cells(picture, 1, 1) == 1


def test_check_constraints():
    picture1 = [[-1, 0, 1, -1],
                [0, 1, -1, 1],
                [1, 0, 1, 0]]

    picture2 = [[0, 0, 1, 1],
                [0, 1, 1, 1],
                [1, 0, 1, 0]]

    assert check_constraints(picture1, {(0, 3, 5), (1, 2, 5), (2, 0, 1)}) == 0
    assert check_constraints(picture2, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 1
    assert check_constraints(picture1, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 2


def test_solve_puzzle():
    assert solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (0, 0, 0)}, 3, 4) == [[0, 0, 1, 1], [0, 1, 1, 1],
                                                                                [1, 0, 1, 0]]
    assert solve_puzzle({(0, 3, 3), (1, 2, 5), (2, 0, 1), (2, 3, 5)}, 3, 4) is None
    assert solve_puzzle({(0, 2, 3), (1, 1, 4), (2, 2, 5)}, 3, 3) == [[0, 0, 1], [1, 1, 1], [1, 1, 1]]
    assert solve_puzzle({(1, 1, 1)}, 2, 2) == [[-1, 0],
                                               [0, 1]]
