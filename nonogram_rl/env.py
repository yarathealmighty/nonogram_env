import gym
from gym import spaces
import numpy as np
from typing import Optional
from .board import Board, TileState


class NonogramEnv(gym.Env):
    metadata = {"render.modes": ["ansi"]}

    def __init__(self, rows=5, cols=5, seed: Optional[int] = None):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.seed = seed
        self.total_points = 0

        self.board = Board(rows, cols)
        self.board.generate_tilemap(fill_prob=0.4, seed=seed)

        self.observation_space = spaces.Box(low=-1, high=1, shape=(rows, cols), dtype=np.int8)
        self.action_space = spaces.Tuple((
            spaces.Discrete(rows),
            spaces.Discrete(cols),
            spaces.Discrete(3)
        ))
        self._gameover = False

    def reset(self, *, seed: Optional[int] = None, options=None):
        super().reset(seed=seed)
        self.total_points = 0
        self.board.generate_tilemap(fill_prob=0.4, seed=seed or self.seed)
        return self._get_obs(), {}

    def step(self, action):
        row, col, mark_idx = action
        if mark_idx == 0:
            mark = TileState.UNMARKED
        elif mark_idx == 1:
            mark = TileState.FILLED
        else:
            mark = TileState.EMPTY

        already_correct = (self.board._tilemap[row][col] == self.board._solution_tilemap[row][col] and
                        self.board._tilemap[row][col] == TileState.FILLED and mark == TileState.FILLED)

        correct = self.board.apply_action(row, col, mark)

        if already_correct:
            reward = -1
        else:
            reward = 1 if correct else -1

        self.total_points += reward

        terminated = self.board.is_solved()

        if terminated:
            self._gameover = True

        truncated = False
        info = {}

        return self._get_obs(), reward, terminated, truncated, info


    def _get_obs(self):
        return np.array(self.board.tilemap, dtype=np.int8)

    def render(self, mode="ansi"):
        """
        Renders the board showing the player's marks.
        - White: UNMARKED
        - Green: FILLED
        - Red: EMPTY
        Displays row and column hints.
        Uses 3x3 “pixel” blocks per tile.
        Shows the solution if the game has ended.
        """
        ANSI_RESET = "\033[0m"
        COLORS = {
            TileState.UNMARKED: "\033[47m",  # white
            TileState.FILLED: "\033[42m",    # green
            TileState.EMPTY: "\033[41m",     # red
        }

        rows = self.board._rows
        cols = self.board._cols
        max_row_hint_len = max(len(h) for h in self.board.horizontal_hints)
        max_col_hint_len = max(len(h) for h in self.board.vertical_hints)

        # Render column hints
        col_hint_lines = []
        for i in range(max_col_hint_len):
            line = [" " * 3 * max_row_hint_len]
            for c in range(cols):
                hints = self.board.vertical_hints[c]
                val = hints[i - (max_col_hint_len - len(hints))] if i >= max_col_hint_len - len(hints) else " "
                line.append(f"{val:^3}")
            col_hint_lines.append("".join(line))

        for l in col_hint_lines:
            print(l)

        # Render player board with row hints
        for r in range(rows):
            row_hints = self.board.horizontal_hints[r]
            padded_hints = [""] * (max_row_hint_len - len(row_hints)) + [str(h) for h in row_hints]
            hint_str = "".join(f"{h:>3}" for h in padded_hints)

            for i in range(3):
                line = [hint_str if i == 1 else " " * 3 * max_row_hint_len]
                for c in range(cols):
                    player_mark = self.board._tilemap[r][c]
                    color = COLORS[player_mark]
                    line.append(color + "   " + ANSI_RESET)
                print("".join(line))

        print(f"Points: {self.total_points}\n")

        # Show the solution when the game ended
        if self._gameover:
            print("Game ended! Original solution:")
            for r in range(rows):
                for i in range(3):
                    line = [" " * 3 * max_row_hint_len]
                    for c in range(cols):
                        solution_mark = self.board._solution_tilemap[r][c]
                        color = COLORS[solution_mark]
                        line.append(color + "   " + ANSI_RESET)
                    print("".join(line))
            print()



    def close(self):
        pass
