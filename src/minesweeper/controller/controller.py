from tkinter import *

from minesweeper.model.gameconfig import GameConfig
from minesweeper.model.minesweeper import Minesweeper, SquareState, GameState
from minesweeper.view.main_menu import MainMenu
from minesweeper.view.game import GameWindow

class Controller():
    def __init__(self) -> None:
        self.root = Tk()
        self.main_menu = MainMenu(self.root)
        self.game_window = GameWindow(self.root)
        self.config = GameConfig()
        self.model = None
        self.first_click = True

    def start(self):
        self.set_main_menu_bindings()
        self.root.mainloop()

    def set_main_menu_bindings(self):
        self.main_menu.beginner.bind("<Button>", func=self.play_beginner)
        self.main_menu.intermediate.bind("<Button>", func=self.play_intermediate)
        self.main_menu.advanced.bind("<Button>", func=self.play_advanced)

    def play_beginner(self, event):
        self.config.set_to_beginner()
        self.new_game()

    def play_intermediate(self, event):
        self.config.set_to_intermediate()
        self.new_game()

    def play_advanced(self, event):
        self.config.set_to_advanced()
        self.new_game()

    def new_game(self):
        self.main_menu.update_instructions()
        self.game_window.open_new_game_window(self.config.columns, self.config.rows)
        self.model = Minesweeper(self.config)
        self.set_minesweeper_square_bindings()
        self.set_reset_button_binding()
        self.game_window.set_mines_remaining(self.model.mines_remaining)
        self.first_click = True

    def set_minesweeper_square_bindings(self):
        for row in range(self.config.rows):
            for column in range(self.config.columns):
                self.game_window.squares[f"{column},{row}"].bind(
                    "<Button>", 
                    func = lambda event, column=column, row=row: self.square_click(event, column, row)
                )
    
    def set_reset_button_binding(self):
        self.game_window.reset_button.bind("<Button>", func=self.reset)

    def square_click(self, event, column, row):
        if (self.model.game_state != GameState.ACTIVE): return
        if (event.num == 1):
            # Left click
            if (self.first_click):
                self.model.set_grid_values(column, row)
                self.first_click = False

            updated_squares = self.model.reveal_square(column, row)
        else:
            # Right click
            self.model.set_or_clear_flag(column, row)
            updated_squares = [(column, row)]
            self.game_window.set_mines_remaining(self.model.mines_remaining)

        self.update_button_displays(updated_squares)
        if (self.model.game_state == GameState.LOST):
            self.game_window.set_loser_display()
            self.reveal_all_squares()
        else:
            self.model.check_for_win()
            if (self.model.game_state == GameState.WON):
                self.game_window.set_winner_display()

    def update_button_displays(self, updated_squares: list[tuple[int, int]]):
        for square in updated_squares:
            column = square[0]
            row = square[1]
            square_state = self.model.get_square_state(column, row)
            if (square_state == SquareState.HIDDEN):
                self.game_window.set_square_hidden(column, row)
            if (square_state == SquareState.REVEALED):
                self.game_window.set_square_display_number_or_mine(
                    column, 
                    row, 
                    self.model.get_square_value(column, row)
                )
            if (square_state == SquareState.FLAGGED):
                self.game_window.set_square_flagged(column, row)

    def reveal_all_squares(self):
        for column in range(self.model.columns):
            for row in range(self.model.rows):
                self.game_window.set_square_display_number_or_mine(
                    column, 
                    row, 
                    self.model.get_square_value(column, row)
                )

    def reset(self, event):
        self.new_game()
