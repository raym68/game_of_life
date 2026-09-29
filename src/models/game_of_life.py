"""Conway's Game of Life rules and toroidal grid model."""

from __future__ import annotations

import random


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 760
PANEL_HEIGHT = 60
CELL_SIZE = 10
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - PANEL_HEIGHT) // CELL_SIZE
BACKGROUND_COLOR = (18, 20, 28)
GRID_COLOR = (38, 42, 55)
CELL_COLOR = (100, 220, 150)
TEXT_COLOR = (235, 238, 245)


class GameOfLife:
    """Store and update a cellular automaton on a toroidal grid."""

    def __init__(self, width: int, height: int) -> None:
        """Create an empty grid with the given dimensions."""
        self.width = width
        self.height = height
        self.cells = [[False for _ in range(width)] for _ in range(height)]

    def toggle_cell(self, column: int, row: int, alive: bool) -> None:
        """Set a cell's state when its coordinates are inside the grid."""
        if 0 <= column < self.width and 0 <= row < self.height:
            self.cells[row][column] = alive

    def randomize(self, probability: float = 0.22) -> None:
        """Randomly populate the grid using the given live-cell probability."""
        self.cells = [
            [random.random() < probability for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def clear(self) -> None:
        """Set every cell to dead."""
        self.cells = [[False for _ in range(self.width)] for _ in range(self.height)]

    def count_neighbors(self, column: int, row: int) -> int:
        """Count neighbors, wrapping row and column indexes at the edges."""
        return sum(
            self.cells[(row + row_offset) % self.height][
                (column + column_offset) % self.width
            ]
            for row_offset in (-1, 0, 1)
            for column_offset in (-1, 0, 1)
            if row_offset != 0 or column_offset != 0
        )

    def step(self) -> None:
        """Advance the simulation by one generation using Conway's rules."""
        next_cells = [[False for _ in range(self.width)] for _ in range(self.height)]
        for row in range(self.height):
            for column in range(self.width):
                neighbors = self.count_neighbors(column, row)
                next_cells[row][column] = neighbors == 3 or (
                    self.cells[row][column] and neighbors == 2
                )
        self.cells = next_cells

    def alive_count(self) -> int:
        """Return the number of live cells."""
        return sum(sum(row) for row in self.cells)
