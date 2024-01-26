from minesweeper.sprites import TileSheets, TileBuilder

from game.model.minesweeper import Minesweeper, SquareState

class GameWindow():
    def __init__(self, screen, top_buffer) -> None:
        self.screen = screen
        self.top_buffer = top_buffer

        tile_design = TileSheets(TileSheets.two_thousand)
        tile_builder = TileBuilder(tile_design)
        self.tile = tile_builder.build()

        self.blit = lambda img, idx, row: screen.blit(img, (16 * idx, (row * 16)+self.top_buffer))

    def draw_all_tiles(self, model: Minesweeper):
        # TODO generally bad practice to directly use the model in view 
        for column in range(model.columns):
            for row in range(model.rows):
                state = model.get_square_state(column, row)
                value = model.get_square_value(column, row)
                self._draw_tile(column, row, state, value)

    def _draw_tile(self, column: int, row: int, state: SquareState, value: int):
        if state == SquareState.FLAGGED:
            self.blit(self.tile.flag, column, row)
        elif state == SquareState.HIDDEN:
            self.blit(self.tile.unopened, column, row)
        elif value < 0:
            self.blit(self.tile.mine_red, column, row)
        else: 
            self.blit(self.tile[value], column, row)
