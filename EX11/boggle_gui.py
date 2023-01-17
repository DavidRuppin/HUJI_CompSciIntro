import abc
from dataclasses import dataclass
import tkinter as tk
from tkinter import Toplevel

from boggle_board_randomizer import randomize_board


@dataclass
class BoardUIConstants:
    BOGGLE_GAME_TITLE = 'Boggle'
    TIMER_LABEL_TEXT  = 'Time left:'
    SCORE_LABEL_TEXT = 'Score:'
    BOARD_BUTTON_SIZE = 5

@dataclass
class MenuUIConstants:
    MENU_TITLE_TEXT = 'Boggle Menu'
    START_NEW_GAME_BUTTON = 'Play Boggle!'

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
        new_window_button = tk.Button(self.root, text=MenuUIConstants.START_NEW_GAME_BUTTON, command=self.start_new_game)
        new_window_button.pack(expand=True, padx=0, pady=0)

    def start_new_game(self):
        # Create a new Toplevel window
        BoggleGame(self.root)

    def start(self):
        # Start the Tkinter main loop
        self.root.mainloop()


class BoggleGame:
    def __init__(self, root):
        self.ui = BoardUI(tk.Toplevel(root))

class BoardUI:
    def __init__(self, new_window: tk.Toplevel):
        # Set the title of the window
        new_window.title(BoardUIConstants.BOGGLE_GAME_TITLE)
        # Set the size of the window
        new_window.geometry('200x200')  # Width x Height

        self.window = new_window

        # TODO - Rethink where this needs to happen
        self.board = randomize_board()

        self.init_board()
        self.init_score()
        self.init_timer()

        # Start the timer
        self.timer()

    def init_board(self):
        # Configure the rows and columns to fill the window
        for i in range(len(self.board)):
            self.window.grid_rowconfigure(i + 1, weight=1)
            for j in range(len(self.board[i])):
                self.window.grid_columnconfigure(j, weight=1)

        # Create buttons for each item on the game board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                b = tk.Button(self.window, text=self.board[i][j], command=lambda i=i, j=j: self.button_clicked(i, j),
                              padx=0, pady=0, width=BoardUIConstants.BOARD_BUTTON_SIZE, height=BoardUIConstants.BOARD_BUTTON_SIZE)
                b.grid(row=i + 1, column=j, sticky="nsew")

    def init_timer(self, time=10):
        self.time = time

        # Create the timer label
        self.timer_label = tk.Label(self.window, text=f"{BoardUIConstants.TIMER_LABEL_TEXT} {self.time}")
        self.timer_label.grid(row=0, column=1, columnspan=len(self.board[0]), sticky="nsew")

    def init_score(self, score=0):
        self.score = score

        # Create the score label
        self.score_label = tk.Label(self.window, text=f"{BoardUIConstants.SCORE_LABEL_TEXT} {self.score}")
        self.score_label.grid(row=0, column=0, sticky="nsew")
    def button_clicked(self, i, j):
        print(f'Button {i}, {j} clicked!')
        # update the score
        self.score += 1
        self.score_label.config(text=f"{BoardUIConstants.SCORE_LABEL_TEXT} {self.score}")

    def get_window(self) -> Toplevel:
        return self.window

    def timer(self):
        if self.time > 0:
            self.time -= 1
            self.timer_label.config(text=f"{BoardUIConstants.TIMER_LABEL_TEXT} {self.time}")
            # Runs this function again in 1 second
            self.window.after(1000, self.timer)
        else:
            # Updating the function in real time
            self.button_clicked = lambda *args: print('Can\'t do shit bruv')


menu = MenuUI()

menu.start()
