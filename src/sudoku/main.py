"""Sudoku solver. lets you enter a sudoku board and watch it get solved."""

import logging
import sys

import pygame
from pygame import display

from sudoku.constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Set up basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logger.info("hello world")


def main() -> None:
    """Driver function for asteroids game."""
    logger.info("Starting asteroids")

    _ = pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("white")

        for thing in updatable:
            thing.update(dt)

        for thing in asteroids:
            for s in shots:
                if s.is_colliding(thing):
                    s.kill()
                    thing.split()

            if player.is_colliding(thing):
                logging.info("Game over!")
                sys.exit(0)

        for thing in drawable:
            thing.draw(screen)

        display.flip()
        dt = clock.tick() / 1000


if __name__ == "__main__":
    main()
