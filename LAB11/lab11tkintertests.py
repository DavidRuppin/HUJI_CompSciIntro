#################################################################
# FILE : lab11tkintertests.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex11 2022-2023
#################################################################

import tkinter as tk
from tkinter import ttk

def on_item_click(event):
    item = tree.identify_row(event.y)
    print("You clicked on row", item)

root = tk.Tk()
tree = ttk.Treeview(root, columns=("col1", "col2", "col3"), show="headings")
tree.heading("#1", text="Column 1")
tree.heading("#2", text="Column 2")
tree.heading("#3", text="Column 3")
tree.insert("", "end", values=("Value 1", "Value 2", "Value 3"))
tree.insert("", "end", values=("Value 4", "Value 5", "Value 6"))
tree.insert("", "end", values=("Value 7", "Value 8", "Value 9"))
tree.bind("<Button-1>", on_item_click)
tree.pack(expand=True, fill='both')
root.mainloop()
