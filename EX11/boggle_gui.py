import abc
import tkinter as tk

class FrameElement(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_frame(self) -> tk.Frame:
        raise NotImplementedError

class BoggleGUI:
    def __init__(self):
        window = tk.Tk()
        window.title('Boggle')
        self.window = window

    def start(self):
        self.window.mainloop()

    def show_frame(self, frame_element: FrameElement):
        frame_element.get_frame().pack(fill=tk.BOTH, )


class BoardUI():
    def __init__(self):
        frame = tk.Frame()
        frame.winfo_toplevel().geometry('')
        self.frame = frame

        # Create a 2D array to represent the game board
        board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        # Create a function to handle button clicks
        def button_clicked(i, j):
            print(f'Button {i}, {j} clicked!')

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

    def get_frame(self) -> tk.Frame:
        return self.frame


b = BoggleGUI()
c = BoardUI()
b.show_frame(c)
b.start()

