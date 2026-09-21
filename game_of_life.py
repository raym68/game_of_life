"""Conway's Game of Life with a toroidal grid.

Install the only dependency once:
    pip install pygame

Controls:
    Space  — start/pause simulation
    Left mouse button — draw live cells
    Right mouse button — erase cells
    R — fill the grid randomly
    C — clear the grid
    Up/Down — change simulation speed
    N — make one step while paused
"""

from __future__ import annotations

import random

import pygame


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
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells = [[False for _ in range(width)] for _ in range(height)]

    def toggle_cell(self, column: int, row: int, alive: bool) -> None:
        if 0 <= column < self.width and 0 <= row < self.height:
            self.cells[row][column] = alive

    def randomize(self, probability: float = 0.22) -> None:
        self.cells = [
            [random.random() < probability for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def clear(self) -> None:
        self.cells = [[False for _ in range(self.width)] for _ in range(self.height)]

    def count_neighbors(self, column: int, row: int) -> int:
        """Count neighbors with wrapping at each edge of the field."""
        return sum(
            self.cells[(row + row_offset) % self.height][
                (column + column_offset) % self.width
            ]
            for row_offset in (-1, 0, 1)
            for column_offset in (-1, 0, 1)
            if row_offset != 0 or column_offset != 0
        )

    def step(self) -> None:
        next_cells = [[False for _ in range(self.width)] for _ in range(self.height)]
        for row in range(self.height):
            for column in range(self.width):
                neighbors = self.count_neighbors(column, row)
                next_cells[row][column] = neighbors == 3 or (
                    self.cells[row][column] and neighbors == 2
                )
        self.cells = next_cells

    def alive_count(self) -> int:
        return sum(sum(row) for row in self.cells)


def draw_game(screen: pygame.Surface, game: GameOfLife) -> None:
    screen.fill(BACKGROUND_COLOR)
    for row, cells in enumerate(game.cells):
        for column, is_alive in enumerate(cells):
            rectangle = pygame.Rect(
                column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            if is_alive:
                pygame.draw.rect(screen, CELL_COLOR, rectangle)
            pygame.draw.rect(screen, GRID_COLOR, rectangle, 1)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Игра Жизнь")
    font = pygame.font.SysFont("Arial", 20)
    clock = pygame.time.Clock()
    game = GameOfLife(GRID_WIDTH, GRID_HEIGHT)
    game.randomize()
    is_running = False
    steps_per_second = 8
    last_step_time = 0
    application_running = True

    while application_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                application_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_running = not is_running
                elif event.key == pygame.K_r:
                    game.randomize()
                elif event.key == pygame.K_c:
                    game.clear()
                    is_running = False
                elif event.key == pygame.K_UP:
                    steps_per_second = min(30, steps_per_second + 1)
                elif event.key == pygame.K_DOWN:
                    steps_per_second = max(1, steps_per_second - 1)
                elif event.key == pygame.K_n and not is_running:
                    game.step()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if mouse_y < GRID_HEIGHT * CELL_SIZE:
            column = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE
            if buttons[0]:
                game.toggle_cell(column, row, True)
            elif buttons[2]:
                game.toggle_cell(column, row, False)

        current_time = pygame.time.get_ticks()
        if is_running and current_time - last_step_time >= 1000 // steps_per_second:
            game.step()
            last_step_time = current_time

        draw_game(screen, game)
        status = "запущена" if is_running else "на паузе"
        text = (
            f"Симуляция: {status} | Живых клеток: {game.alive_count()} | "
            f"Скорость: {steps_per_second} шаг/с"
        )
        controls = "Space — пауза, ЛКМ — добавить, ПКМ — стереть, R — случайно, C — очистить"
        screen.blit(font.render(text, True, TEXT_COLOR), (10, WINDOW_HEIGHT - 53))
        screen.blit(font.render(controls, True, TEXT_COLOR), (10, WINDOW_HEIGHT - 27))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
