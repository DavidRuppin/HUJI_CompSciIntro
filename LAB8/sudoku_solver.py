#################################################################
# FILE : sudoku_solver.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex8 2022-2023
#################################################################
from pprint import pprint
from typing import List

board = [[0, 0, 0, 0, 0, 3, 0, 1, 7],
         [0, 1, 5, 0, 0, 9, 0, 0, 8],
         [0, 6, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 7, 0, 0, 0],
         [0, 0, 9, 0, 0, 0, 2, 0, 0],
         [0, 0, 0, 5, 0, 0, 0, 0, 4],
         [0, 0, 0, 0, 0, 0, 0, 2, 0],
         [5, 0, 0, 6, 0, 0, 3, 4, 0],
         [3, 4, 0, 2, 0, 0, 0, 0, 0]]

SIZE: int = len(board)
VALUES = range(1, 10)


def is_value_ok_at(board: List[List[int]], row: int, col: int, value: int):
    block_row_start = (row // 3) * 3
    block_col_start = (col // 3) * 3

    for x in range(block_row_start, block_row_start + 3):
        for y in range(block_col_start, block_col_start + 3):
            if x != row and y != col and board[x][y] == value:
                return False

    # Going over entire row and col
    for i in range(SIZE):
        if i != row and board[i][col] == value:
            return False
        if i != col and board[row][i] == value:
            return False

    return True


def solve_sudoku_helper(sudoku: List[List[int]], index: int = None):
    if index is None:
        index = 0

    if index == SIZE * SIZE:
        return True

    row = index // 9
    col = index % 9

    for value in VALUES:
        res = False
        if is_value_ok_at(sudoku, row, col, value):
            sudoku[row][col] = value
            res = solve_sudoku_helper(sudoku, index + 1)
        if res is True:
            return res

    sudoku[row][col] = 0


def solve_sudoku(sudoku: List[List[int]]):
    solve_sudoku_helper(sudoku)
    pprint(sudoku)
