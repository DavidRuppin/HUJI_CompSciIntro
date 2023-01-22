"""
Web Pages Used: https://web.archive.org/web/20190515013614id_/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html
"""

from dataclasses import dataclass
import tkinter as tk
from tkinter import Toplevel, ttk
from typing import Iterable, Set

from EX11.ex11_utils import load_boggle_dictionary
from game_objects import Board, Location, Path
from boggle_board_randomizer import randomize_board


@dataclass
class GameUIConstants:
    
    GAME_WINDOW_GEOMETRY = '400x400'
    BOGGLE_GAME_TITLE = 'Current Word'

    DEFAULT_TIMER = 180
    TIMER_LABEL_TEXT = 'Time left:'

    DEFAULT_SCORE = 0
    SCORE_LABEL_TEXT = 'Score:'

    USED_WORDS_TITLE_TEXT = 'Used Words'

    BOARD_BUTTON_SIZE = 5
    BUTTON_MIDDLE_CLICK_EVENT = '<Button-2>'
    BUTTON_RIGHT_CLICK_EVENT = '<Button-3>'


@dataclass
class MenuUIConstants:
    MENU_TITLE_TEXT = 'Boggle Menu'
    START_NEW_GAME_BUTTON = 'Play Boggle!'

    MENU_RULES_TEXT = 'This is boggle! A game of finding words in a random board using neighboring letters.  ' \
                        'You can LEFT CLICK a slot to add it to your current path, RIGHT CLICK any slot to submit' \
                      'your current word (If the word is in our dictionary your score will increase, how exciting!). ' \
                        'and use the MIDDLE CLICK on any part of the board to toggle the used words view. Good luck!'

class MenuUI:
    def __init__(self):
        # Initialize the root window and set its properties
        self.root = self.init_root()
        self.init_widgets()

    def init_root(self) -> tk.Tk:
        # Create the Tkinter root window
        root = tk.Tk()
        # Get the screen width and height
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        # Set the size of the window to be half of the screen width and height
        root.geometry(f'{self.width // 4}x{self.height // 4}')
        # Set the title of the window
        root.title(MenuUIConstants.MENU_TITLE_TEXT)
        return root

    def init_widgets(self):
        # Create the button that opens the new window
        new_window_button = tk.Button(self.root, text=MenuUIConstants.START_NEW_GAME_BUTTON,
                                      command=self.start_new_game)
        new_window_button.grid(row=0, column=0)
        self.root.grid_columnconfigure(0, weight=1)

        rules_label = tk.Label(self.root, text=MenuUIConstants.MENU_RULES_TEXT, wraplength=self.width // 2)
        rules_label.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)

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
        if word in self.get_words() and (not word in self.get_used_words()):
            # add word to used words
            self.add_path_to_score(word)
            return True

        self.reset_curr_path()
        return False


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
        self.game.finish_word()
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


class GameUI:
    def __init__(self, new_window: tk.Toplevel, board: Board):
        # Set the title of the window
        new_window.title(GameUIConstants.BOGGLE_GAME_TITLE)
        # Set the size of the window
        new_window.geometry(GameUIConstants.GAME_WINDOW_GEOMETRY)  # Width x Height

        self.window = new_window
        self.board = board._board
        self.prev_click = None

        self.init_board()
        self.init_score()
        self.init_timer_label()
        self.init_used_words_container()

    def init_board(self):
        # Configure the rows and columns to fill the window
        for i in range(len(self.board)):
            self.window.grid_rowconfigure(i + 1, weight=1)
            for j in range(len(self.board[i])):
                self.window.grid_columnconfigure(j, weight=1)

        # Create buttons for each item on the game board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                button = tk.Button(self.window, text=self.board[i][j],
                              padx=0, pady=0, width=GameUIConstants.BOARD_BUTTON_SIZE,
                              height=GameUIConstants.BOARD_BUTTON_SIZE)

                # Configuring the default button action command
                button.config(command=lambda loc=Location(i, j): self.board_button_clicked(loc))
                # And the right click button action command
                button.bind(GameUIConstants.BUTTON_RIGHT_CLICK_EVENT, lambda event: self.submit_word())
                button.bind(GameUIConstants.BUTTON_MIDDLE_CLICK_EVENT, lambda event: self.toggle_used_words())
                button.grid(row=i + 1, column=j, sticky="nsew")

    def init_timer_label(self):
        # Create the timer label
        self.timer_label = tk.Label(self.window, text=f"{GameUIConstants.TIMER_LABEL_TEXT} {GameUIConstants.DEFAULT_TIMER}")
        self.timer_label.grid(row=0, column=1, columnspan=len(self.board[0]), sticky="nsew")

    def init_score(self):
        # Create the score label
        self.score_label = tk.Label(self.window, text=f"{GameUIConstants.SCORE_LABEL_TEXT} {GameUIConstants.DEFAULT_SCORE}")
        self.score_label.grid(row=0, column=0, sticky="nsew")

    def init_used_words_container(self):
        self.used_words_notebook = ttk.Notebook(self.window)
        self.show_used_words()
        self.used_words_frame = ttk.Frame(self.used_words_notebook)
        self.used_words_list = tk.Listbox(self.used_words_frame)
        self.used_words_list.pack(fill=tk.BOTH, expand=True)
        self.used_words_notebook.add(self.used_words_frame, text=GameUIConstants.USED_WORDS_TITLE_TEXT)

    def get_window(self) -> Toplevel:
        return self.window

    def set_timer(self, time: int):
        self.timer_label.config(text=f'{GameUIConstants.TIMER_LABEL_TEXT} {time}')

    def set_score(self, score: int):
        self.score_label.config(text=f'{GameUIConstants.SCORE_LABEL_TEXT} {score}')

    def set_curr_word(self, word: str):
        self.get_window().title(word)

    def set_used_words(self, words: Iterable[str]):
        self.used_words_list.delete(0, tk.END)
        self.used_words_list.insert(tk.END, *words)
        self.used_words_list.pack()

    def show_used_words(self):
        self.used_words_showing = True
        self.used_words_notebook.grid(row=0, column=len(self.board[0]), rowspan=len(self.board) + 1,
                                      padx=5, pady=5, sticky="nsew")

    def hide_used_words(self):
        self.used_words_showing = False
        self.used_words_notebook.grid_forget()

    def toggle_used_words(self):
        if self.used_words_showing:
            self.hide_used_words()
        else:
            self.show_used_words()

    def board_button_clicked(self, button_location: Location):
        pass

    def submit_word(self):
        print('submit word')

    def set_board_button_function(self, func):
        self.board_button_clicked = func

    def set_submit_word_action(self, func):
        self.submit_word = func



if __name__ == '__main__':
    # print(load_boggle_dictionary("boggle_dict.txt")

    menu = MenuUI()

    menu.start()


