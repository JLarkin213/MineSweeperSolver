from tkinter import *
from tkinter import font as tkFont

class GameWindow(Toplevel):
    def __init__(self, root: Tk):
        self.root = root
        self.window_open = False
        self.num_columns = 0
        self.num_rows = 0
        self.square_window_size_multiplier = 28
        self.squares = {}

        self.top_panel_frame = None
        self.game_frame = None

        self.top_panel_height = 2

        self.color_dict = {
            -1: "red2", 0: "grey1", 1:"blue", 2:"green", 3:"red", 4:"navy", 5:"maroon", 6: "turquoise3", 7:"red4", 8: "grey1"
        }

    def open_new_game_window(self, num_columns: int, num_rows: int):
        self.num_columns = num_columns
        self.num_rows = num_rows

        if self.window_open:
            self.destroy()
        super().__init__(master = self.root)
        self.window_open = True

        self.title("PLAY!")
        self.set_window_geometry()
        self.display_top_panel()
        self.display_new_grid()

    def set_window_geometry(self):
        height = (self.num_rows * self.square_window_size_multiplier) + 30
        width = self.num_columns * self.square_window_size_multiplier
        self.geometry(f"{width}x{height}")

    def display_top_panel(self):
        self.top_panel_frame = Frame(self)
        self.top_panel_frame.grid(row=0)
        self.create_mines_remaining()
        self.create_reset_button()
        self.create_timer()

    def create_mines_remaining(self):
        self.mines_remaining_label = Label(self.top_panel_frame, text="00", bg="red4", fg="red2", height=self.top_panel_height)
        self.mines_remaining_label.grid(column=0, row=0)

    def create_reset_button(self):
        self.reset_button = Button(self.top_panel_frame, text="RESET", height=self.top_panel_height)
        self.reset_button.grid(column=1, row=0)

    def create_timer(self):
        self.timer_label = Label(self.top_panel_frame, text="000", bg="red4", fg="red2", height=self.top_panel_height)
        self.timer_label.grid(column=2, row=0)

    def display_new_grid(self):
        self.game_frame = Frame(self)
        self.game_frame.grid(row=1)
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                self.create_single_square(x, y)

    def create_single_square(self, column: int, row: int):
        self.squares[f"{column},{row}"] = Label(
            self.game_frame,
            text=" ",
            bg="gray70",
            borderwidth=2,
            relief="raised",
            height=1,
            width=2,
            padx=1,
            pady=1,
        )
        self.squares[f"{column},{row}"].grid(column=column, row=row, padx=1, pady=1, ipadx=1, ipady=1)
    
    def set_square_hidden(self, column: int, row: int):
        self.squares[f"{column},{row}"].configure(text=" ", bg="gray70", relief="raised")

    def set_square_flagged(self, column: int, row: int):
        flag_font = tkFont.Font(weight='bold', size=12, underline=True)
        self.squares[f"{column},{row}"].configure(text="F", font=flag_font, fg="red2")

    def set_square_display_number_or_mine(self, column: int, row: int, value):
        text_color = self.color_dict[value]
        value_font = tkFont.Font(weight='bold', size=12)
        if (value == -1):
            value = "X"
        self.squares[f"{column},{row}"].configure(
            text=f"{value}",
            bg="gray80",
            fg=text_color,
            font=value_font,
            relief="sunken",
        )

    def set_mines_remaining(self, mines_remaining: int):
        if (mines_remaining < 10):
            mines_remaining = f"0{mines_remaining}"
        self.mines_remaining_label.configure(text=f"{mines_remaining}")

    def reset_top_panel(self):
        self.top_panel_frame.destroy()
        self.top_panel_frame = Frame(self)
        self.top_panel_frame.grid(row=0)

    def set_winner_display(self):
        self.reset_top_panel()
        Label(self.top_panel_frame, text="WIN!!", fg="green2", height=self.top_panel_height).grid()

    def set_loser_display(self):
        self.reset_top_panel()
        Label(self.top_panel_frame, text="LOSS!!", fg="red2", height=self.top_panel_height).grid()
