import abc
from dataclasses import dataclass
import tkinter as tk
from tkinter import Toplevel

from EX11.boggle_board_randomizer import randomize_board


@dataclass
class Constants:
    START_GAME_BUTTON_TEXT = 'Start Game!'
    TIMER_LABEL_ANCHOR = 'e'
    TIMER_LABEL_TEXT  = 'Time left:'
    SCORE_LABEL_ANCHOR = 'w'
    SCORE_LABEL_TEXT = 'Score:'
    BOARD_BUTTON_SIZE = 5


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
        root.title("Boggle Menu")
        return root


    def init_widgets(self):
        # Create the button that opens the new window
        new_window_button = tk.Button(self.root, text="Open new window", command=self.open_new_window)
        new_window_button.pack(expand=True, padx=0, pady=0)

    def open_new_window(self):
        # Create a new Toplevel window
        new_window = BoardUI(self.root).get_window()
        # Set the title of the window
        new_window.title("New Window")
        # Set the size of the window
        new_window.geometry("200x200") # Width x Height

    def start(self):
        # Start the Tkinter main loop
        self.root.mainloop()


class BoardUI:
    def __init__(self, root: tk.Tk):
        new_window = tk.Toplevel(root)
        new_window.winfo_toplevel().geometry('')
        self.window = new_window
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
                              padx=0, pady=0, width=Constants.BOARD_BUTTON_SIZE, height=Constants.BOARD_BUTTON_SIZE)
                b.grid(row=i + 1, column=j, sticky="nsew")

    def init_timer(self, time=10):
        self.time = time

        # Create the timer label
        self.timer_label = tk.Label(self.window, text=f"{Constants.TIMER_LABEL_TEXT} {self.time}")
        self.timer_label.grid(row=0, column=1, columnspan=len(self.board[0]), sticky="nsew")

    def init_score(self, score=0):
        self.score = score

        # Create the score label
        self.score_label = tk.Label(self.window, text=f"{Constants.SCORE_LABEL_TEXT} {self.score}")
        self.score_label.grid(row=0, column=0, sticky="nsew")
    def button_clicked(self, i, j):
        print(f'Button {i}, {j} clicked!')
        # update the score
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def get_window(self) -> Toplevel:
        return self.window

    def timer(self):
        if self.time > 0:
            self.time -= 1
            self.timer_label.config(text=f"Time: {self.time}")
            # Runs this function again in 1 second
            self.window.after(1000, self.timer)
        else:
            # Updating the function in real time
            self.button_clicked = lambda *args: print('Can\'t do shit bruv')


menu = MenuUI()

menu.start()
