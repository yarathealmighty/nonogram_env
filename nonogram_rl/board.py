import random
from enum import IntEnum
from typing import Optional


class TileState(IntEnum):
    UNMARKED = 0   # white tile
    FILLED = 1     # green tile
    EMPTY = -1     # red tile


class Board:
    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._solution_tilemap = None
        self._tilemap = [[TileState.UNMARKED for _ in range(cols)] for _ in range(rows)]
        self.vertical_hints = []
        self.horizontal_hints = []

    @property
    def tilemap(self):
        return self._tilemap

    @property
    def solution_tilemap(self):
        return "we don't do that around here."

    def generate_tilemap(self, fill_prob: float = 0.5, seed: Optional[int] = None):
        """Generate deterministic puzzle using a seed."""
        rng = random.Random(seed)

        self._solution_tilemap = [
            [TileState.FILLED if rng.random() < fill_prob else TileState.EMPTY
             for _ in range(self._cols)]
            for _ in range(self._rows)
        ]

        self._tilemap = [[TileState.UNMARKED for _ in range(self._cols)] for _ in range(self._rows)]

        self.horizontal_hints = [self._generate_hints(row) for row in self._solution_tilemap]
        self.vertical_hints = [
            self._generate_hints([self._solution_tilemap[r][c] for r in range(self._rows)])
            for c in range(self._cols)
        ]

    def _generate_hints(self, line):
        hints = []
        count = 0
        for cell in line:
            if cell == TileState.FILLED:
                count += 1
            elif count > 0:
                hints.append(count)
                count = 0
        if count > 0:
            hints.append(count)
        return hints


    def apply_action(self, row: int, col: int, mark: TileState) -> bool:
        """
        Player marks a cell. Returns True if correct, False otherwise.
        """
        self._tilemap[row][col] = mark
        return self._solution_tilemap[row][col] == mark

    def is_solved(self) -> bool:
        """
        Returns True if all tiles have been marked (not UNMARKED),
        regardless of whether they match the solution.
        """
        for r in range(self._rows):
            for c in range(self._cols):
                if self._tilemap[r][c] == TileState.UNMARKED:
                    return False
        return True