"""Functions for drawing the Game of Life interface."""

import pygame

from src.models.game_of_life import (
    BACKGROUND_COLOR,
    CELL_COLOR,
    CELL_SIZE,
    GRID_COLOR,
    PANEL_HEIGHT,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    GameOfLife,
)


def draw_game(
    screen: pygame.Surface,
    game: GameOfLife,
    font: pygame.font.Font,
    is_running: bool,
    steps_per_second: int,
) -> None:
    """Draw the grid, live cells, simulation status, and controls."""
    screen.fill(BACKGROUND_COLOR)
    for row, cells in enumerate(game.cells):
        for column, is_alive in enumerate(cells):
            rectangle = pygame.Rect(
                column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            if is_alive:
                pygame.draw.rect(screen, CELL_COLOR, rectangle)
            pygame.draw.rect(screen, GRID_COLOR, rectangle, 1)

    status = "запущена" if is_running else "на паузе"
    text = (
        f"Симуляция: {status} | Живых клеток: {game.alive_count()} | "
        f"Скорость: {steps_per_second} шаг/с"
    )
    controls = "Space — пауза, ЛКМ — добавить, ПКМ — стереть, R — случайно, C — очистить"
    screen.blit(font.render(text, True, TEXT_COLOR), (10, WINDOW_HEIGHT - PANEL_HEIGHT + 7))
    screen.blit(font.render(controls, True, TEXT_COLOR), (10, WINDOW_HEIGHT - 33))

