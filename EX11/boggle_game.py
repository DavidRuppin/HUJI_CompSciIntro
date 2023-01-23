#################################################################
# FILE : boggle_game.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex11 2022-2023
#################################################################
import tkinter as tk
from dataclasses import dataclass
from typing import Iterable, Set, Tuple

from boggle_board_randomizer import randomize_board
from boggle_game_ui import GameUI
from boggle_menu_ui import MenuUI
from ex11_utils import load_boggle_dictionary
from game_objects import Board, Location, Path

@dataclass
class BoggleConstants:
    SUCCESSFUL_WORD_ANIMATION_COLOR = 'green'
    FAILED_WORD_ANIMATION_COLOR = 'red'

class BoggleGame:
    def __init__(self, board: Board, words: Iterable[str]):
        self.board = board
        self._words = words
        self._score = 0
        self.curr_path: Path = []
        self.used_words: Set[str] = set()

    def _can_add_to_curr_path(self, location: Location) -> bool:
        if not self.curr_path:
            return True

        if not self.board.is_location_in_board(location):
            return False

        if location not in self.curr_path and self.board.are_neighbors(self.curr_path[-1], location):
                return True

        return False

    def add_location_to_path(self, location: Location) -> bool:
        if self._can_add_to_curr_path(location):
            self.curr_path.append(location)
            return True
        return False


    def get_curr_word(self) -> str:
        return self.board.word_from_locations(self.curr_path)

    def finish_word(self) -> Tuple[bool, Path]:
        curr_path = self.curr_path
        word = self.get_curr_word()
        if word in self.get_words() and (not word in self.get_used_words()):
            # add word to used words
            self.add_path_to_score(word)
            return (True, curr_path)

        self.reset_curr_path()
        return (False, curr_path)


    def reset_curr_path(self):
        self.curr_path = list()

    def calc_path_score(self) -> int:
        return len(self.curr_path) ** 2

    def add_path_to_score(self, word: str):
        """
        Assuming the current path is valid when this function is called. Increases the score according to the rules,
        adds the current word to the used words set and resets the current path
        """
        self.used_words.add(word)
        self._score += self.calc_path_score()
        self.reset_curr_path()

    def get_score(self) -> int:
        return self._score

    def get_words(self) -> Iterable[str]:
        return self._words

    def get_used_words(self) -> Set[str]:
        return self.used_words

class BoggleGameController:
    def __init__(self, root):
        self.board = Board(randomize_board())
        self.game = BoggleGame(self.board, load_boggle_dictionary("boggle_dict.txt"))
        self.init_gui(root)
        self.init_timer()

    def init_gui(self, root):
        self.gui = GameUI(tk.Toplevel(root), self.board)
        self.gui.set_board_button_function(self.board_button_clicked)
        self.gui.set_submit_word_action(self.submit_word)

    def init_timer(self):
        self.time = 300
        self.timer()

    def timer(self):
        if self.time > 0:
            self.time -= 1
            self.gui.set_timer(self.time)
            # Runs this function again in 1 second
            self.gui.get_window().after(1000, self.timer)
        else:
            # Stop receiving user input
            self.finish_game()

    def board_button_clicked(self, location: Location):
        if self.game.add_location_to_path(location):
            self.update_ui()

    def submit_word(self):
        success, path = self.game.finish_word()
        if success:
            self.gui.animate_path(path, BoggleConstants.SUCCESSFUL_WORD_ANIMATION_COLOR)
        else:
            self.gui.animate_path(path, BoggleConstants.FAILED_WORD_ANIMATION_COLOR)
        self.update_ui()


    def update_ui(self):
        self.gui.set_curr_word(self.game.get_curr_word())
        self.gui.set_timer(self.time)
        self.gui.set_score(self.game.get_score())
        self.gui.set_used_words(self.game.get_used_words())

    def finish_game(self):
        empty_lambda = lambda *args, **kwargs: None
        self.gui.set_submit_word_action(empty_lambda)
        self.gui.set_board_button_function(empty_lambda)


if __name__ == '__main__':
    menu = MenuUI()
    menu.start()