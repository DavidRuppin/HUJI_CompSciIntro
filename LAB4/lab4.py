# ----------------------------------------------------#
# FILE : lab4.py
# WRITER : David Ruppin , ruppin , 322296336
# EXERCISE : intro2cs1 exlab4 2023 
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED:
# NOTES:
# ----------------------------------------------------#

from typing import Tuple

BOARD_HEIGHT = 4
BOARD = []


def run_game():
    global BOARD
    BOARD = init_board()
    while not is_board_empty():
        get_next_player()
    print("You won!")


def init_board():
    # Returns a two dimensional array of 1-3-5-7 "matches"
    return [[1] * (i*2 + 1) for i in range(0, 4)]


def get_next_player():
    # Prints the board, gets input and updates the board accordingly
    print_board()
    row, amount = get_input()
    update_board(row, amount)


def print_board():
    print(BOARD)


def is_board_empty() -> bool:
    # Checking for any non-empty row
    for row in BOARD:
        if len(row) > 0:
            return False

    return True


def get_input() -> Tuple[int, int]:
    # Getting user input. If entered incorrectly try again
    user_input_row = input("Which row do you choose? (1-n) ")
    if check_row_number_validity(user_input_row):
        row = int(user_input_row) - 1
        user_input_amount = input("How many matches would you like? (1-n) ")
        if check_amount_taken(user_input_amount, row):
            return row, int(user_input_amount)

    return get_input()


def check_row_number_validity(raw_input) -> bool:
    return True if raw_input.isnumeric() and 1 <= int(raw_input) <= len(BOARD) else False


def check_amount_taken(raw_input, row) -> bool:
    return True if raw_input.isnumeric() and 1 <= int(raw_input) <= len(BOARD[row]) else False


def update_board(row, amount):
    for i in range(amount):
        BOARD[row].pop()
