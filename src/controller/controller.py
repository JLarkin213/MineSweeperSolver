# Import Module
from tkinter import *
from model.gameconfig import GameConfig
from model.minesweeper import Minesweeper, SquareState, GameState
from view.screens.main_menu import MainMenu
from view.screens.game import GameWindow

class Controller():
    def __init__(self) -> None:
        self.root = Tk()
        self.main_menu = MainMenu(self.root)
        self.game_window = GameWindow(self.root)
        self.config = GameConfig()
        self.model = None

    def start(self):
        self.set_main_menu_bindings()
        self.root.mainloop()

    def set_main_menu_bindings(self):
        self.main_menu.beginner.bind("<Button>", func=self.play_beginner)
        self.main_menu.intermediate.bind("<Button>", func=self.play_intermediate)
        self.main_menu.advanced.bind("<Button>", func=self.play_advanced)

    def set_minesweeper_square_bindings(self):
        for row in range(self.config.rows):
            for column in range(self.config.columns):
                self.game_window.squares[f"{column},{row}"].bind(
                    "<Button>", 
                    func = lambda event, column=column, row=row: self.square_click(event, column, row)
                )

    def play_beginner(self, event):
        self.config.set_to_beginner()
        self._play()

    def play_intermediate(self, event):
        self.config.set_to_intermediate()
        self._play()

    def play_advanced(self, event):
        self.config.set_to_advanced()
        self._play()

    def square_click(self, event, column, row):
        print(f"you clicked button {event.num}, at {column} X {row}")
        if (event.num == 1):
            # Left click
            pass
        else:
            # Right click
            pass

    def _play(self):
        self.main_menu.update_instructions()
        self.model = Minesweeper(self.config)
        self.game_window.open_new_game_window(self.config.columns, self.config.rows)
        self.set_minesweeper_square_bindings()
