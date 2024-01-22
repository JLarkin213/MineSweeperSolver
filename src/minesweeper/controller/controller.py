from tkinter import *

from minesweeper.model.gameconfig import GameConfig
from minesweeper.model.minesweeper import Minesweeper, SquareState, GameState
from minesweeper.view.main_menu import MainMenu
from minesweeper.view.game import GameWindow

class Controller():
    def __init__(self) -> None:
        self.config = GameConfig()
        self.model = None
        self.first_click = True
        self.active_display = False

    def start_with_display(self):
        self.root = Tk()
        self.main_menu = MainMenu(self.root)
        self.game_window = GameWindow(self.root)
        self._set_main_menu_bindings()
        self.active_display = True

        self.root.mainloop()

    def _new_game(self):
        self.model = Minesweeper(self.config)
        self.first_click = True

        if self.active_display: 
            self.main_menu.update_instructions()
            self.game_window.open_new_game_window(self.config.columns, self.config.rows)
            self._set_minesweeper_square_bindings()
            self._set_reset_button_binding()
            self.game_window.set_mines_remaining(self.model.mines_remaining)

    def square_click(self, click_type, column, row):
        if (self.model.game_state != GameState.ACTIVE): return
        if (click_type == "left"):
            if (self.first_click):
                self.model.set_grid_values(column, row)
                self.first_click = False

            updated_squares = self.model.reveal_square(column, row)
        else:
            self.model.set_or_clear_flag(column, row)
            updated_squares = [(column, row)]

        return updated_squares
    
    def _update_display_after_square_click(self, updated_squares: list[tuple[int, int]]):
        self._update_button_displays(updated_squares)
        self.game_window.set_mines_remaining(self.model.mines_remaining)
        if (self.model.game_state == GameState.LOST):
            self.game_window.set_loser_display()
            self._reveal_all_squares()
        else:
            self.model.check_for_win()
            if (self.model.game_state == GameState.WON):
                self.game_window.set_winner_display()

    def _close_windows(self):
        if self.active_display:
            self.game_window.destroy()
            self.root.destroy()

    def _set_main_menu_bindings(self):
        self.main_menu.beginner.bind("<Button>", func=self._play_beginner)
        self.main_menu.intermediate.bind("<Button>", func=self._play_intermediate)
        self.main_menu.advanced.bind("<Button>", func=self._play_advanced)

    def _play_beginner(self, event=None):
        self.config.set_to_beginner()
        self._new_game()

    def _play_intermediate(self, event=None):
        self.config.set_to_intermediate()
        self._new_game()

    def _play_advanced(self, event=None):
        self.config.set_to_advanced()
        self._new_game()

    def _set_minesweeper_square_bindings(self):
        for row in range(self.config.rows):
            for column in range(self.config.columns):
                self.game_window.squares[f"{column},{row}"].bind(
                    "<Button>", 
                    func = lambda event, column=column, row=row: self._square_click(event, column, row)
                )
    
    def _set_reset_button_binding(self):
        self.game_window.reset_button.bind("<Button>", func=self._reset)

    def _square_click(self, event, column, row):
        if (event.num == 1):
            updated_squares = self._square_click("left", column, row)
        else:
            updated_squares = self._square_click("right", column, row)

        self._update_display_after_square_click(updated_squares)

    def _update_button_displays(self, updated_squares: list[tuple[int, int]]):
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

    def _reveal_all_squares(self):
        for column in range(self.model.columns):
            for row in range(self.model.rows):
                self.game_window.set_square_display_number_or_mine(
                    column, 
                    row, 
                    self.model.get_square_value(column, row)
                )

    def _reset(self, event=None):
        self._new_game()
