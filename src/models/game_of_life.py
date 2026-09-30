"""Правила игры «Жизнь» Конвея и модель поля с тороидальной геометрией."""

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
    """Хранит и обновляет клеточный автомат на тороидальном поле."""

    def __init__(self, width: int, height: int) -> None:
        """Создать пустое поле заданного размера."""
        self.width = width
        self.height = height
        self.cells = [[False for _ in range(width)] for _ in range(height)]

    def toggle_cell(self, column: int, row: int, alive: bool) -> None:
        """Задать состояние клетки, если её координаты находятся внутри поля."""
        if 0 <= column < self.width and 0 <= row < self.height:
            self.cells[row][column] = alive

    def randomize(self, probability: float = 0.22) -> None:
        """Случайно заполнить поле с заданной вероятностью появления живой клетки."""
        self.cells = [
            [random.random() < probability for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def clear(self) -> None:
        """Сделать все клетки мёртвыми."""
        self.cells = [[False for _ in range(self.width)] for _ in range(self.height)]

    def count_neighbors(self, column: int, row: int) -> int:
        """Подсчитать соседей, переходя к противоположному краю у границ поля."""
        return sum(
            self.cells[(row + row_offset) % self.height][
                (column + column_offset) % self.width
            ]
            for row_offset in (-1, 0, 1)
            for column_offset in (-1, 0, 1)
            if row_offset != 0 or column_offset != 0
        )

    def step(self) -> None:
        """Выполнить один шаг симуляции по правилам Конвея."""
        next_cells = [[False for _ in range(self.width)] for _ in range(self.height)]
        for row in range(self.height):
            for column in range(self.width):
                neighbors = self.count_neighbors(column, row)
                next_cells[row][column] = neighbors == 3 or (
                    self.cells[row][column] and neighbors == 2
                )
        self.cells = next_cells

    def alive_count(self) -> int:
        """Вернуть количество живых клеток."""
        return sum(sum(row) for row in self.cells)
