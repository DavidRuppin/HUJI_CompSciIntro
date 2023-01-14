#################################################################
# FILE : boggle_main.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex11 2022-2023
#################################################################

from EX11.boggle_board_randomizer import randomize_board
from game_objects import *


def get_random_board() -> Board:
    return Board(randomize_board())
