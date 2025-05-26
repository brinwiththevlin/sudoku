"""Sudoku game."""
import logging

from pathlib import Path
import pygame
from pygame import display

from sudoku.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from sudoku.screen_manager import ScreenManager
from sudoku.screens import HomeScreen, PlayScreen, LoadScreen

# Set up basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logger.info("hello world")


def main() -> None:
    """Driver function for sudoku game."""
    logger.info("Starting sudoku")

    _ = pygame.init()

    window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = ScreenManager(window)
    manager.register_screen("play", PlayScreen)
    manager.register_screen("home", HomeScreen)
    manager.register_screen("load", LoadScreen)

    puzzles_path = Path(__file__).parent.parent.parent / "puzzles"

    manager.switch_to("home", {})

    # TODO(brinhasavlin): add a reset button to reset the puzzle
    # TODO(brinhasavlin): add a solve button to solve the puzzle (add a solver function)

    while True:
        manager.handle_events()
        manager.update(0)
        manager.draw()

        display.flip()


if __name__ == "__main__":
    main()
