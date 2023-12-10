
class GameConfig():
    def __init__(self) -> None:
        self.columns = 0
        self.rows = 0
        self.mines = 0

    def set_to_beginner(self):
        self.columns = 8
        self.rows = 8
        self.mines = 10

    def set_to_intermediate(self):
        self.columns = 16
        self.rows = 16
        self.mines = 40

    def set_to_advanced(self):
        self.columns = 16
        self.rows = 30
        self.mines = 99

    def set_to_custom(self, columns: int, rows: int, mines: int):
        self.columns = columns
        self.rows = rows
        self.mines = mines
