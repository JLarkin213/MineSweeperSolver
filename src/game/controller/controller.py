import math

import pygame

from game.model.gameconfig import GameConfig
from game.model.minesweeper import Minesweeper, GameState
from game.view.gamewindow import GameWindow


class Controller():
    def __init__(self) -> None:
        self.config = GameConfig()
        self.first_click = True
        self.model = None

        self.pygame = None
        self.clock = None
        self.game_window = None
        self.screen = None
        self.active_display = False

        self.top_buffer = 60

    def start_for_normal_user(self):
        self.new_game()

        self.init_pygame()

        self._run()

    def init_pygame(self):
        self.pygame = pygame
        self.pygame.init()
        self.pygame.display.init()
        self.screen = self.pygame.display.set_mode(
            (self.config.columns*16, self.config.rows*16+self.top_buffer)
        )
        self.clock = self.pygame.time.Clock()
        self.game_window = GameWindow(self.screen, self.top_buffer)
        
    def _run(self):
        self.active_display = True
        while self.active_display:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.active_display = False

                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    column = math.floor(event.dict["pos"][0]/16)
                    row = math.floor((event.dict["pos"][1]-self.top_buffer)/16)
                    if row < 0:
                        print(f"click in menu space {event}")
                    elif event.dict["button"] == 1:
                        print(f"left click - column: {column} row: {row}")
                        self.update_model_after_square_click("left", column, row)
                    elif (event.dict["button"] == 3):
                        print(f"right click - column: {column} row: {row}")
                        self.update_model_after_square_click("right", column, row)

            self.render_display()

            self.clock.tick(5)  # limits FPS to 5

    def render_display(self):
        self.screen.fill("black")
        self.game_window.draw_all_tiles(self.model)
        if not self.active_display:
            self.pygame.event.pump()
        self.pygame.display.flip()

    def new_game(self):
        self.model = Minesweeper(self.config)
        self.first_click = True

    def update_model_after_square_click(self, click_type, column, row) -> list[tuple[int, int]]:
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
    