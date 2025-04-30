"""Board and Cell classes."""

from typing import override

import pygame

from sudoku.game_sprites import GameSprite
from sudoku.groups import drawable, updatable


class Cell(GameSprite):
    """Cell class for sudoku board."""

    def __init__(self, x: int, y: int, width: int, height: int, value: int| None = None)  -> None:
        """Initialize the cell with its position and value."""
        super().__init__()
        updatable.add(self)
        drawable.add(self)
        self.x: int = x
        self.y: int = y
        self.value: int | None =  value
        self.width: int = width
        self.height: int = height

    @override
    def draw(self, screen: pygame.Surface) -> None:
        """Draw cell on the screen.

        draws the cell on the screen, with a magin around the board

        Args:
            screen: game window
        """
        # TODO(brinhasavlin): add display of value
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        _ = pygame.draw.rect(screen, "white", rect)
        _ = pygame.draw.rect(screen, "black", rect, width=3)

    @override
    def update(self, value: int) -> None:
        """Update the value of the cell.

        Args:
            value: new value
        """
        # TODO(brinhasavlin): update i think that update should somehow involve getting user imput.
        self.value = value
