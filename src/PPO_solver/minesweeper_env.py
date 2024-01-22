from gymnasium import Env, spaces
import numpy as np

from minesweeper.controller.controller import Controller
from minesweeper.model.minesweeper import SquareState, GameState

class MinesweeperEnv(Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None) -> None:
        self.minesweeper = Controller()
        self.minesweeper.config.set_to_intermediate()
        self.config = self.minesweeper.config

        self.number_of_squares = self.config.columns * self.config.rows
        self.max_cordinate = max([self.config.rows, self.config.columns])

        # action is [left or right click, column, row]
        self.action_space = spaces.MultiDiscrete([2, self.config.columns-1, self.config.rows-1])
        self.observation_space = spaces.Dict(
            {
                "mines_remaining": spaces.Discrete(1),
                "grid": spaces.Dict({
                    # [[state or value, column, row]*self.number_of_squares]
                    "states": spaces.Box(0, self.max_cordinate, shape=(self.number_of_squares, 3), dtype=int),
                    "values": spaces.Box(0, self.max_cordinate, shape=(self.number_of_squares, 3), dtype=int)
                }),
            }
        )

        self.square_state_to_int = {
            SquareState.HIDDEN: 0,
            SquareState.REVEALED: 1,
            SquareState.FLAGGED: 2,
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if self.render_mode == "human":
            self.minesweeper.close_windows()
            self.minesweeper.start()
  
        self.minesweeper.new_game()
        return self._get_observation(), {}
    
    def step(self, action):
        click_type = "left" if (action[1] == 1) else "right"
        column = action[2]
        row = action[3]

        revealed_squares = self.minesweeper.square_click(click_type, column, row)
        num_of_revealed_squares = len(revealed_squares)

        if (self.minesweeper.model.game_state == GameState.ACTIVE):
            reward = num_of_revealed_squares
            terminated = False
        elif (self.minesweeper.model.game_state == GameState.WON):
            reward = num_of_revealed_squares + 50
            terminated = True
        else: # GameState is LOST
            reward = -50
            terminated = True

        if self.render_mode == "human":
            self.minesweeper.update_display_after_square_click(revealed_squares)

        return self._get_observation(), reward, terminated, False, {}

    def _get_observation(self):
        states = []
        values = []
        for column in range(self.config.columns):
            for row in range(self.config.rows):
                state = self.minesweeper.model.get_square_state(column, row)
                states.append[self.square_state_to_int[state], column, row]

                if state == SquareState.REVEALED:
                    values.append[self.minesweeper.model.get_square_value(column, row), column, row]
                else:
                    values.append[0, column, row]

        return {
            "mines_remaining": self.minesweeper.model.mines_remaining,
            "grid": {
                "states": np.array([states]),
                "values": np.array([values])
            }
        }
    