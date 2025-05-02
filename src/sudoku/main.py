"""Sudoku solver. lets you enter a sudoku board and watch it get solved."""

import logging
from pathlib import Path

import pygame
from pygame import display

from sudoku.board import Board
from sudoku.cell import Cell
from sudoku.constants import SCREEN_HEIGHT, SCREEN_WIDTH, XMARGIN, YMARGIN
from sudoku.groups import drawable, selectable

# Set up basic configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logger.info("hello world")


def main() -> None:  # noqa: C901, PLR0912
    """Driver function for sudoku game."""
    logger.info("Starting sudoku")

    _ = pygame.init()

    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    board = Board(XMARGIN, YMARGIN)
    # if puzzle.txt exists at project root load it
    if Path("puzzle.txt").exists():
        with Path("puzzle.txt").open() as f:
            lines = f.readlines()
            board.load(lines)
    # set title of window
    display.set_caption("Sudoku Solver")

    while True:
        for event in pygame.event.get():
            # TODO(brinhasavlin): add multi highlighting.
            # when user click a number highligh (not select) all of the same number
            # TODO(brinhasavlin): add more controls (i.e. annotation, multi select)
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                [s.unselect() for s in selectable]
                for s in selectable:
                    if s.rect.collidepoint(*pos):
                        s.select()
                        if type(s) is Cell:
                            board.highlight(s.value)
                        break
                else:
                    board.highlight(0)
            if event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    digit = event.key - pygame.K_0
                    for s in selectable:
                        if s.selected:
                            s.update(digit)
                if event.key == pygame.K_BACKSPACE:
                    for s in selectable:
                        if s.selected:
                            s.update(0)

        _ = screen.fill("green" if board.solved(logger) else (200, 10, 50))

        for d in drawable:
            d.draw(screen)

        display.flip()


if __name__ == "__main__":
    main()
