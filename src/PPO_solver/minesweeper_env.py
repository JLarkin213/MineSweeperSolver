from gymnasium import Env, spaces

from game.controller.controller import Controller
from game.model.minesweeper import SquareState, GameState

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
        self.unflattend_observation_space = spaces.Dict(
            {
                "mines_remaining": spaces.Discrete(self.config.mines+1),
                # [[column, row, value]*self.number_of_squares] ***value here is different than the game code
                "grid": spaces.Box(0, self.max_cordinate, shape=(self.number_of_squares, 3), dtype=int)
            }
        )
        self.observation_space = spaces.flatten_space(self.unflattend_observation_space)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        print("INIT ENV")

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.minesweeper.new_game()

        if self.render_mode == "human":
            if self.minesweeper.pygame == None: self.minesweeper.init_pygame()
            self.render()
  
        return self._get_observation(), {}
    
    def step(self, action):
        click_type = "left" if (action[0] == 1) else "right"
        column = action[1]
        row = action[2]

        first_click = self.minesweeper.first_click

        revealed_squares = self.minesweeper.update_model_after_square_click(
            click_type, column, row
        )

        if (self.minesweeper.model.game_state == GameState.ACTIVE):
            reward = self._determine_reward(first_click, click_type, column, row, revealed_squares)
            terminated = False
        elif (self.minesweeper.model.game_state == GameState.WON):
            reward = 10
            terminated = True
        else: # GameState is LOST
            reward = -10
            terminated = True

        if self.render_mode == "human":
            self.render()

        return self._get_observation(), (reward/10), terminated, False, {}

    def _get_observation(self):
        grid = []
        for column in range(self.config.columns):
            for row in range(self.config.rows):
                state = self.minesweeper.model.get_square_state(column, row)
                if (state == SquareState.HIDDEN):
                    value = -1
                elif (state == SquareState.FLAGGED):
                    value = -2
                elif (state == SquareState.REVEALED):
                    value = self.minesweeper.model.get_square_value(column, row)
                    # bombs represented with value -1 in the game code but I like this better for the obs space. 
                    if (value == -1): value = -3

                grid.append([column, row, value])

        unflat_space = {
            "mines_remaining": self.minesweeper.model.mines_remaining,
            "grid": grid
        }
        return spaces.flatten(self.unflattend_observation_space, unflat_space)
    
    def close(self):
        if self.render_mode == "human":
            self.minesweeper.pygame.quit()

    def render(self):
        self.minesweeper.render_display()
        self.minesweeper.clock.tick(1)
    
    def _determine_reward(
            self,
            first_click: bool,
            click_type: str,
            column: int,
            row: int,
            revealed_squares: list[tuple[int, int]]
        ) -> int:
        if (len(revealed_squares) == 0): return -1

        if (first_click): return 0

        if (click_type == "right"):
            flagged_value = self.minesweeper.model.get_square_value(column, row)
            state = self.minesweeper.model.get_square_state(column, row)
            # if it flagged a bomb correctly reward
            if (flagged_value == -1 and state == SquareState.FLAGGED): return 3
            else: return -5

        # left click that revealed squares
        self.was_not_random = False

        def were_squares_next_to_it_already_revealed(adjecent_column, adjecent_row):
            adjecent_state = self.minesweeper.model.get_square_state(adjecent_column, adjecent_row)
            if (
                adjecent_state == SquareState.REVEALED 
                and (adjecent_column, adjecent_row) not in revealed_squares
            ):
                self.was_not_random = True

        self.minesweeper.model.evaluate_adjecent_squares(column, row, were_squares_next_to_it_already_revealed)
        if (self.was_not_random): return 3
        else: return -3
    