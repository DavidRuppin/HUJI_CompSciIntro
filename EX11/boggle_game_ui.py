#################################################################
# FILE : boggle_game_ui.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex11 2022-2023
#################################################################

import tkinter as tk

from tkinter import ttk
from dataclasses import dataclass
from game_objects import Board, Location
from typing import Iterable, Set


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

    def get_window(self) -> tk.Toplevel:
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

