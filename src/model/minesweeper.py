import random

from model.gameconfig import GameConfig

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
    Params:
    rows: Int The number of rows on the board
    columns: Int The number of columns on the board
    mines: Int The number of mines on the board
    Important info:
    explain the self.grid
    """
    def __init__(self, config: GameConfig) -> None:
        self.rows = config.rows
        self.columns = config.columns
        self.mines = config.mines
        self.create_new_grid()
        self.game_state = GameState.ACTIVE

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
        for column in range(self.columns):
            for row in range(self.rows):
                if (self.get_square_value(column, row) == -1): continue
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

                        if (self.get_square_value(adjecent_column, adjecent_row) == -1):
                            self.grid[row][column]["value"] += 1

    def get_square_value(self, column: int, row: int) -> int:
        return self.grid[row][column]["value"]
    
    def get_square_state(self, column: int, row: int) -> SquareState:
        return self.grid[row][column]["state"]
    
    def update_square_state(self, column: int, row: int, new_state: SquareState):
        """
        Updates the state of the sqaure in the grid and update the game state if it was lost
        """
        self.grid[row][column]["state"] = new_state
        if (new_state == SquareState.REVEALED and self.get_square_value(column, row) == -1):
            self.game_state = GameState.LOST
    
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