"""Sudoku game."""
import logging

# from pathlib import Path
import pygame
from pygame import display

from sudoku.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from sudoku.screen_manager import ScreenManager
from sudoku.screens import HomeScreen, PlayScreen, LoadScreen, SolverScreen

# Set up basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logger.info("hello world")


def main() -> None:
    """Driver function for sudoku game."""
    logger.info("Starting sudoku")

    _ = pygame.init()

    clock = pygame.time.Clock()

    window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = ScreenManager(window)
    manager.register_screen("play", PlayScreen)
    manager.register_screen("home", HomeScreen)
    manager.register_screen("load", LoadScreen)
    manager.register_screen("solver", SolverScreen)

    # puzzles_path = Path(__file__).parent.parent.parent / "puzzles"

    manager.switch_to("home", {})
    dt = 0

    # TODO(brinhasavlin): add a `solve` button to solve the puzzle (add a solver function)

    while True:
        manager.handle_events()
        manager.update(dt)
        manager.draw()

        display.flip()
        dt = clock.tick() / 1000


if __name__ == "__main__":
    main()
