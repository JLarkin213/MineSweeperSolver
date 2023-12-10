from tkinter import *

class GameWindow(Toplevel):
    def __init__(self, root: Tk):
        self.root = root
        self.window_open = False
        self.num_columns = 0
        self.num_rows = 0
        self.square_window_size_multiplier = 45
        self.squares = {}

    def open_new_game_window(self, num_columns: int, num_rows: int):
        self.num_columns = num_columns
        self.num_rows = num_rows

        if self.window_open:
            self.destroy()
        super().__init__(master = self.root)
        self.window_open = True

        self.title("PLAY!")
        self.set_window_geometry()
        self.display_grid()

    def set_window_geometry(self):
        height = (self.num_rows * self.square_window_size_multiplier) + 100
        width = self.num_columns * self.square_window_size_multiplier
        self.geometry(f"{width}x{height}")

    def create_single_square(self, column, row):
        self.squares[f"{column},{row}"] = Button(
            self,
            height=2,
            width=1
        )
        self.squares[f"{column},{row}"].grid(column=column, row=row, padx=0, pady=0)

    def display_grid(self):
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                self.create_single_square(x, y)

# disable button
# button.state(['disabled'])
