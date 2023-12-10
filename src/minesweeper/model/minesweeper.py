import random

from minesweeper.model.gameconfig import GameConfig

class SquareState():
    HIDDEN = "h"
    REVEALED = "r"
    FLAGGED = "f"

class GameState():
    WON = "w"
    LOST = "l"
    ACTIVE = "a"

class Minesweeper(object):
    """
    A model for a Minesweeper board.
    Important info:
    explain the self.grid
    """
    def __init__(self, config: GameConfig) -> None:
        self.rows = config.rows
        self.columns = config.columns
        self.mines = config.mines
        self.create_new_grid()
        self.game_state = GameState.ACTIVE
        self.mines_remaining = self.mines

    def create_new_grid(self):
        self.grid = self.create_empty_grid()
        self.add_mines()
        self.add_number_of_adjecent_mines()

    def create_empty_grid(self):
        grid = []
        for i in range(self.rows):
            column = []
            for i in range(self.columns):
                column.append({"value": 0, "state": SquareState.HIDDEN})
            grid.append(column)
        return grid

    def add_mines(self):
        added_mines = 0
        while added_mines < self.mines:
            column = random.randint(0, self.columns-1)
            row = random.randint(0, self.rows-1)
            if (self.get_square_value(column, row) != -1):
                self.grid[row][column]["value"] = -1
                added_mines += 1
    
    def add_number_of_adjecent_mines(self):
        def increment_value_if_adjecent_square_is_mine(adjecent_column, adjecent_row):
             if (self.get_square_value(adjecent_column, adjecent_row) == -1):
                            self.grid[row][column]["value"] += 1

        for column in range(self.columns):
            for row in range(self.rows):
                if (self.get_square_value(column, row) == -1): continue
                self.evaluate_adjecent_squares(column, row, increment_value_if_adjecent_square_is_mine)

    def get_square_value(self, column: int, row: int) -> int:
        return self.grid[row][column]["value"]
    
    def get_square_state(self, column: int, row: int) -> SquareState:
        return self.grid[row][column]["state"]
    
    def update_square_state(self, column: int, row: int, new_state: SquareState):
        self.grid[row][column]["state"] = new_state
    
    def reveal_square(self, column: int, row: int):
        self.just_revealed_squares = []
        self._reveal_square(column, row)
        return self.just_revealed_squares
    
    def _reveal_square(self, column: int, row: int):
        square_state = self.get_square_state(column, row)
        if (square_state == SquareState.FLAGGED): return
        square_value = self.get_square_value(column, row)

        if (square_state == SquareState.HIDDEN):
            self.update_square_state(column, row, SquareState.REVEALED)
            self.just_revealed_squares.append((column, row))
            if (square_value == -1):
                self.game_state = GameState.LOST
            elif (square_value == 0):
                self.reveal_adjecent_squares(column, row)
        elif (self.get_number_of_adjecent_flags(column, row) == square_value):
            self.reveal_adjecent_squares(column, row)

    def reveal_adjecent_squares(self,column: int, row: int):
        def reveal_adjecent_square(adjecent_column, adjecent_row):
            if (self.get_square_state(adjecent_column, adjecent_row) != SquareState.REVEALED):
                self._reveal_square(adjecent_column, adjecent_row)

        self.evaluate_adjecent_squares(column, row, reveal_adjecent_square)

    def get_number_of_adjecent_flags(self, column: int, row: int) -> int:
        self.number_of_adjecent_flags = 0
        
        def is_adjecent_square_flagged(adjecent_column, adjecent_row):
            if (self.get_square_state(adjecent_column, adjecent_row) == SquareState.FLAGGED):
                self.number_of_adjecent_flags += 1

        self.evaluate_adjecent_squares(column, row, is_adjecent_square_flagged)

        return self.number_of_adjecent_flags
    
    def evaluate_adjecent_squares(self, column: int, row: int, func):
        for column_increment in [-1, 0, 1]:
            for row_increment in [-1, 0, 1]:
                # Don't analyze the square we are trying to determine the number of adjecent mines for
                if (column_increment == 0 and row_increment == 0): continue
                adjecent_column = column+column_increment
                # Column is out of bounds
                if (adjecent_column < 0 or adjecent_column >= self.columns): continue
                adjecent_row = row+row_increment
                # Row is out of bounds
                if (adjecent_row < 0 or adjecent_row >= self.rows): continue

                func(adjecent_column, adjecent_row)
    
    def set_or_clear_flag(self, column: int, row: int):
        square_state = self.get_square_state(column, row)
        if (square_state == SquareState.HIDDEN):
            self.flag_square(column, row)
        elif (square_state == SquareState.FLAGGED):
            self.unflag_square(column, row)
    
    def flag_square(self, column: int, row: int):
        self.mines_remaining -= 1
        self.update_square_state(column, row, SquareState.FLAGGED)
    
    def unflag_square(self, column: int, row: int):
        self.mines_remaining += 1
        self.update_square_state(column, row, SquareState.HIDDEN)
    
    def check_for_win(self):
    # Loses are checked every time a mine is revealed so we only need to check for the win condition here
        for row in self.grid:
            for square in row:
                if (square["state"] == SquareState.HIDDEN and square["value"] != -1):
                    self.game_state = GameState.ACTIVE
                    return False
        self.game_state = GameState.WON

    def print_grid(self):
        for x in self.grid:
            print(x)


if __name__ == "__main__":
    m = Minesweeper(10, 5, 2)
    m.create_new_grid()
    m.print_grid()