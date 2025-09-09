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
        truncated = False
        info = {}

        return self._get_obs(), reward, terminated, truncated, info


    def _get_obs(self):
        return np.array(self.board.tilemap, dtype=np.int8)

    def render(self, mode="ansi"):
        ANSI_RESET = "\033[0m"
        COLORS = {
            "UNMARKED": "\033[47m",
            "CORRECT": "\033[42m",
            "INCORRECT": "\033[41m",
        }

        rows = self.board._rows
        cols = self.board._cols
        max_row_hint_len = max(len(h) for h in self.board.horizontal_hints)
        max_col_hint_len = max(len(h) for h in self.board.vertical_hints)

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

        for r in range(rows):
            row_hints = self.board.horizontal_hints[r]
            padded_hints = [""] * (max_row_hint_len - len(row_hints)) + [str(h) for h in row_hints]
            hint_str = "".join(f"{h:>3}" for h in padded_hints)
            for i in range(3):
                line = [hint_str if i == 1 else " " * 3 * max_row_hint_len]
                for c in range(cols):
                    player_mark = self.board._tilemap[r][c]
                    solution_mark = self.board._solution_tilemap[r][c]
                    if player_mark == TileState.UNMARKED:
                        color = COLORS["UNMARKED"]
                    elif player_mark == solution_mark:
                        color = COLORS["CORRECT"]
                    else:
                        color = COLORS["INCORRECT"]
                    line.append(color + "   " + ANSI_RESET)
                print("".join(line))

        print(f"Points: {self.total_points}\n")

    def close(self):
        pass
