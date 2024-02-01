from gymnasium import Env, spaces

from game.controller.controller import Controller
from game.model.minesweeper import SquareState, GameState

class MinesweeperEnv(Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None, mines_overide=None) -> None:
        self.minesweeper = Controller()
        self.minesweeper.config.set_to_beginner()
        if (mines_overide):
            self.minesweeper.config.mines = mines_overide

        self.config = self.minesweeper.config

        self.number_of_squares = self.config.columns * self.config.rows
        self.max_cordinate = max([self.config.rows, self.config.columns])

        # action is [column, row]
        self.action_space = spaces.MultiDiscrete([self.config.columns-1, self.config.rows-1])

        self.unflat_observation_space = spaces.Box(-3, 8, shape=(self.config.columns, self.config.rows), dtype=int)

        self.observation_space = spaces.flatten_space(self.unflat_observation_space)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        print("INIT ENV")

        self.steps_this_episode = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.minesweeper.new_game()

        if self.render_mode == "human":
            if self.minesweeper.pygame == None: self.minesweeper.init_pygame()
            self.render()

        self.steps_this_episode = 0
        return self._get_observation(), {"win": False}
    
    def step(self, action):
        if (self.minesweeper.model.game_state != GameState.ACTIVE):
            raise RuntimeError("Trying to perform a step on a game that isn't active???")
            
        click_type = "left" #if (action[0] == 1) else "right"
        column = action[0]
        row = action[1]

        first_click = self.minesweeper.first_click

        revealed_squares = self.minesweeper.update_model_after_square_click(
            click_type, column, row
        )

        win = False
        if (self.minesweeper.model.game_state == GameState.ACTIVE):
            reward = self._determine_reward(first_click, click_type, column, row, revealed_squares)
            terminated = False
        elif (self.minesweeper.model.game_state == GameState.WON):
            reward = 1
            terminated = True
            win = True
        else: # GameState is LOST
            reward = -1
            terminated = True

        if self.render_mode == "human":
            self.render()

        self.steps_this_episode += 1
        truncated = (self.steps_this_episode>self.number_of_squares)

        return self._get_observation(), reward, terminated, truncated, {"win": win}

    def _get_observation(self):
        grid = []
        for idx in range(self.config.columns):
            column = []
            for row in range(self.config.rows):
                state = self.minesweeper.model.get_square_state(idx, row)
                if (state == SquareState.HIDDEN):
                    value = -1
                elif (state == SquareState.FLAGGED):
                    value = -2
                elif (state == SquareState.REVEALED):
                    value = self.minesweeper.model.get_square_value(idx, row)
                    # bombs represented with value -1 in the game code but I like this better for the obs space. 
                    if (value == -1): value = -3

                column.append(value)
            grid.append(column)

        # mines_remaining = self.minesweeper.model.mines_remaining
        # if (mines_remaining < -self.config.mines):
        #     # prevent overflow of space
        #     print("Policy is placing flags everywhere!!")
        #     mines_remaining = -self.config.mines

        # unflat_space = {
        #     "mines_remaining": mines_remaining,
        #     "grid": grid
        # }
        return spaces.flatten(self.unflat_observation_space, grid)
    
    def close(self):
        if self.render_mode == "human":
            self.minesweeper.pygame.quit()

    def render(self):
        if self.render_mode == "human":
            self.minesweeper.render_display()
            self.minesweeper.clock.tick(6)
    
    def _determine_reward(
            self,
            first_click: bool,
            click_type: str,
            column: int,
            row: int,
            revealed_squares: list[tuple[int, int]]
        ) -> int:
        if (len(revealed_squares) == 0): return -.1

        if (first_click): return .3

        self.was_not_random = False

        def were_squares_next_to_it_already_revealed(adjecent_column, adjecent_row):
            adjecent_state = self.minesweeper.model.get_square_state(adjecent_column, adjecent_row)
            if (
                adjecent_state == SquareState.REVEALED 
                and (adjecent_column, adjecent_row) not in revealed_squares
            ):
                self.was_not_random = True

        self.minesweeper.model.evaluate_adjecent_squares(column, row, were_squares_next_to_it_already_revealed)

        # if (click_type == "right"):
        #     flagged_value = self.minesweeper.model.get_square_value(column, row)
        #     state = self.minesweeper.model.get_square_state(column, row)
        #     # if it flagged a bomb correctly reward
        #     if (flagged_value == -1 and state == SquareState.FLAGGED and self.was_not_random): return 5
        #     else: return -5

        # left click that revealed squares
        if (self.was_not_random): return .3
        else: return -.3
    