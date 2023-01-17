from dataclasses import dataclass
import tkinter as tk
from tkinter import Toplevel
from typing import List, Set, Iterable

from game_objects import Board, Location, Path
from boggle_board_randomizer import randomize_board


@dataclass
class GameUIConstants:
    DEFAULT_SCORE = 0
    DEFAULT_TIMER = 180
    BOGGLE_GAME_TITLE = 'Current Word'
    TIMER_LABEL_TEXT = 'Time left:'
    SCORE_LABEL_TEXT = 'Score:'
    BOARD_BUTTON_SIZE = 5


@dataclass
class MenuUIConstants:
    MENU_TITLE_TEXT = 'Boggle Menu'
    START_NEW_GAME_BUTTON = 'Play Boggle!'

# TODO - Add more words
WORDS = ['BALL', 'TEE', 'FLIP', 'A']

class MenuUI:
    def __init__(self):
        # Initialize the root window and set its properties
        self.root = self.init_root()
        self.init_widgets()

    def init_root(self) -> tk.Tk:
        # Create the Tkinter root window
        root = tk.Tk()
        # Get the screen width and height
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        # Set the size of the window to be half of the screen width and height
        root.geometry(f'{width // 4}x{height // 4}')
        # Set the title of the window
        root.title(MenuUIConstants.MENU_TITLE_TEXT)
        return root

    def init_widgets(self):
        # Create the button that opens the new window
        new_window_button = tk.Button(self.root, text=MenuUIConstants.START_NEW_GAME_BUTTON,
                                      command=self.start_new_game)
        new_window_button.pack(expand=True, padx=0, pady=0)

    def start_new_game(self):
        # Create a new Toplevel window
        BoggleGameController(self.root)

    def start(self):
        # Start the Tkinter main loop
        self.root.mainloop()

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

    def finish_word(self) -> bool:
        word = self.get_curr_word()
        if word in self.get_words() and not word in self.get_used_words():
            self.add_path_to_score(word)
            return True
        return False

    def calc_path_score(self) -> int:
        return len(self.curr_path) ** 2
    def add_path_to_score(self, word: str):
        self.used_words.add(word)
        self._score += self.calc_path_score()
        self.curr_path = set()

    def get_score(self) -> int:
        return self._score

    def get_words(self) -> Iterable[str]:
        return self._words
    def get_used_words(self) -> Set[str]:
        return self.used_words

class BoggleGameController:
    def __init__(self, root):
        self.board = Board(randomize_board())
        self.game = BoggleGame(self.board, WORDS)

        self.init_gui(root)
        self.init_timer()

    def init_gui(self, root):
        self.gui = GameUI(tk.Toplevel(root), self.board)
        self.gui.set_board_button_function(self.board_button_clicked)
        self.gui.set_submit_word_action(self.submit_word)

    def init_timer(self):
        self.time = 20
        self.timer()

    def timer(self):
        # TODO - Finish me
        if self.time > 0:
            self.time -= 1
            text = f"{GameUIConstants.TIMER_LABEL_TEXT} {self.time}"
            self.gui.set_timer(text)
            # Runs this function again in 1 second
            self.gui.get_window().after(1000, self.timer)
        else:
            # Updating the function in real time
            self.button_clicked = lambda *args: print('Can\'t do shit bruv')

    def board_button_clicked(self, location: Location):
        if self.game.add_location_to_path(location):
            self.update_ui()

    def submit_word(self):
        self.game.finish_word()
        self.update_ui()


    def update_ui(self):
        self.gui.set_curr_word(self.game.get_curr_word())
        self.gui.set_timer(self.time)
        self.gui.set_score(self.game.get_score())
        # self.gui.set_used_word(self.game.get_used_words())


class GameUI:
    def __init__(self, new_window: tk.Toplevel, board: Board):
        # Set the title of the window
        new_window.title(GameUIConstants.BOGGLE_GAME_TITLE)
        # Set the size of the window
        new_window.geometry('200x200')  # Width x Height

        self.window = new_window
        self.board = board._board

        self.init_board()
        self.init_score()
        self.init_timer_label()

    def init_board(self):
        # Configure the rows and columns to fill the window
        for i in range(len(self.board)):
            self.window.grid_rowconfigure(i + 1, weight=1)
            for j in range(len(self.board[i])):
                self.window.grid_columnconfigure(j, weight=1)

        # Create buttons for each item on the game board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                b = tk.Button(self.window, text=self.board[i][j], command=lambda loc=Location(i, j): self.board_button_clicked(loc),
                              padx=0, pady=0, width=GameUIConstants.BOARD_BUTTON_SIZE,
                              height=GameUIConstants.BOARD_BUTTON_SIZE)
                b.grid(row=i + 1, column=j, sticky="nsew")

    def init_timer_label(self):
        # Create the timer label
        self.timer_label = tk.Label(self.window, text=f"{GameUIConstants.TIMER_LABEL_TEXT} {GameUIConstants.DEFAULT_TIMER}")
        self.timer_label.grid(row=0, column=1, columnspan=len(self.board[0]), sticky="nsew")

    def init_score(self):
        # Create the score label
        self.score_label = tk.Label(self.window, text=f"{GameUIConstants.SCORE_LABEL_TEXT} {GameUIConstants.DEFAULT_SCORE}")
        self.score_label.grid(row=0, column=0, sticky="nsew")

    def get_window(self) -> Toplevel:
        return self.window

    def set_timer(self, time: int):
        self.timer_label.config(text=f'{GameUIConstants.TIMER_LABEL_TEXT} {time}')

    def set_score(self, score: int):
        self.score_label.config(text=f'{GameUIConstants.SCORE_LABEL_TEXT} {score}')

    def set_curr_word(self, word: str):
        self.get_window().title(word)

    def set_used_word(self, words: Iterable[str]):
        # TODO - Me
        raise NotImplementedError

    def set_board_button_function(self, func):
        self.board_button_clicked = func

    def set_submit_word_action(self, func):
        self.submit_word = func


menu = MenuUI()

menu.start()
