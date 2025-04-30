"""Sudoku solver. lets you enter a sudoku board and watch it get solved."""

import logging
import sys

import pygame
from pygame import display

from sudoku.board import Cell
from sudoku.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from sudoku.groups import drawable

# Set up basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logger.info("hello world")


def main() -> None:
    """Driver function for sudoku game."""
    logger.info("Starting sudoku")

    _ = pygame.init()
    # clock = pygame.time.Clock()

    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    _ = Cell(10, 10, 0, 45, 45)
    # set title of window
    display.set_caption("Sudoku Solver")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        _ = screen.fill("magenta")

        for d in drawable:
            d.draw(screen)




        display.flip()


if __name__ == "__main__":
    main()
