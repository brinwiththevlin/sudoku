"""Sudoku game."""
import logging

import pygame
from pygame import display

from sudoku.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from sudoku.screen_manager import ScreenManager
from sudoku.screens import HomeScreen, PlayScreen

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

    # TODO(brinhasavlin): replace this with home screen when it is ready
    manager.switch_to("play", {"file_name": "puzzle.txt"})
    # set title of window

    # TODO(brinhasavlin): add a menu screen with options
    # TODO(brinhasavlin): add a load button to load a puzzle
    # TODO(brinhasavlin): add a save button to save a puzzle
    # TODO(brinhasavlin): add a reset button to reset the puzzle
    # TODO(brinhasavlin): add a solve button to solve the puzzle (add a solver function)

    while True:
        # TODO(brinhasavlin): when do we switch screens? that would be an event?
        manager.handle_events()
        manager.update(0)
        manager.draw()

        display.flip()


if __name__ == "__main__":
    main()
