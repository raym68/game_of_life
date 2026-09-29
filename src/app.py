"""Pygame application and event loop for Conway's Game of Life."""

import pygame

from src.models.game_of_life import (
    CELL_SIZE,
    GRID_HEIGHT,
    GRID_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    GameOfLife,
)
from src.renderers.renderer import draw_game


class App:
    """Own the window, user input, and simulation lifecycle."""

    def __init__(self) -> None:
        """Initialize the window and a randomized simulation."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Игра Жизнь")
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.game = GameOfLife(GRID_WIDTH, GRID_HEIGHT)
        self.game.randomize()
        self.is_running = False
        self.steps_per_second = 8
        self.last_step_time = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle one Pygame event; return False when the app should quit."""
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.is_running = not self.is_running
            elif event.key == pygame.K_r:
                self.game.randomize()
            elif event.key == pygame.K_c:
                self.game.clear()
                self.is_running = False
            elif event.key == pygame.K_UP:
                self.steps_per_second = min(30, self.steps_per_second + 1)
            elif event.key == pygame.K_DOWN:
                self.steps_per_second = max(1, self.steps_per_second - 1)
            elif event.key == pygame.K_n and not self.is_running:
                self.game.step()
        return True

    def handle_mouse(self) -> None:
        """Apply held mouse buttons to cells within the grid area."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if mouse_y < GRID_HEIGHT * CELL_SIZE:
            column = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE
            if buttons[0]:
                self.game.toggle_cell(column, row, True)
            elif buttons[2]:
                self.game.toggle_cell(column, row, False)

    def run(self) -> None:
        """Run the main event, update, and drawing loop."""
        application_running = True
        while application_running:
            for event in pygame.event.get():
                application_running = self.handle_event(event) and application_running

            self.handle_mouse()
            current_time = pygame.time.get_ticks()
            if self.is_running and current_time - self.last_step_time >= 1000 // self.steps_per_second:
                self.game.step()
                self.last_step_time = current_time

            draw_game(
                self.screen,
                self.game,
                self.font,
                self.is_running,
                self.steps_per_second,
            )
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

