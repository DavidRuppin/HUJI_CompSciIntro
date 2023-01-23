"""
Web Pages Used: https://web.archive.org/web/20190515013614id_/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html
"""

from dataclasses import dataclass
import tkinter as tk

from boggle_game import BoggleGameController



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
        root.geometry(f'{self.width // 2}x{self.height // 2}')
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

