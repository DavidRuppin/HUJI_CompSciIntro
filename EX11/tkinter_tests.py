import tkinter as tk
from boggle_board_randomizer import randomize_board

def create_board_frame(parent: tk.Tk) -> tk.Frame:
    # Create a 2D array to represent the game board
    board = randomize_board()

    # Create a function to handle button clicks
    def button_clicked(i, j):
        print(f'Button {i}, {j} clicked!')

    # Create a tkinter window
    frame = tk.Frame(parent)

    # Configure the rows and columns to fill the window
    for i in range(len(board)):
        frame.grid_rowconfigure(i, weight=1)
        for j in range(len(board[i])):
            frame.grid_columnconfigure(j, weight=1)

    # Create buttons for each item on the game board
    for i in range(len(board)):
        for j in range(len(board[i])):
            b = tk.Button(frame, text=board[i][j], command=lambda i=i, j=j: button_clicked(i, j), padx=0, pady=0)
            b.grid(row=i, column=j, sticky="nsew")

    return frame


def do_two_windows():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f'{width // 2}x{height // 2}')
    root.title("Boggle Menu")

    def open_second_window():
        second_window = tk.Toplevel(root)
        second_window.geometry(f'{int(width // 2.2)}x{int(height // 2.2)}')
        second_window.title("Boggle")

        back_button = tk.Button(second_window, text="Back", command=second_window.destroy)
        back_button.pack()

    open_second_window_button = tk.Button(root, text="Open Second Window", command=open_second_window)
    open_second_window_button.pack()

    root.mainloop()


def do_two_frames():
    import tkinter as tk

    class MainApplication(tk.Frame):
        def __init__(self, parent: tk.Tk, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.init_main_frame()

        def init_main_frame(self):
            self.main_frame = tk.Frame(self.parent)
            self.main_frame.pack(side="top", fill=tk.BOTH, expand=True)

            self.open_second_frame_button = tk.Button(self.main_frame, text="Open Second Frame",
                                                      command=self.open_second_frame)
            self.open_second_frame_button.pack()

        def open_second_frame(self):
            self.main_frame.destroy()
            self.init_second_frame()

        def init_second_frame(self):
            self.second_frame = create_board_frame(self.parent)
            self.second_frame.pack(side="top", fill=tk.BOTH, expand=True)

        def back_to_main(self):
            self.second_frame.destroy()
            self.init_main_frame()

    root = init_root()
    app = MainApplication(root)
    app.pack(side="top", fill=tk.BOTH, expand=True)
    root.mainloop()


def init_root() -> tk.Tk:
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f'{width // 2}x{height // 2}')
    root.title("Boggle Menu")

    return root

do_two_frames()
