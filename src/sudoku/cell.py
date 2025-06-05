"""Cell class for sudoku board."""

from typing import final, override

import pygame
from pygame.font import Font

from sudoku.constants import INVALID_COLOR, LOCK_COLOR, USER_COLOR
from sudoku.game_sprites import GameSprite


@final
class Cell(GameSprite):
    """Cell class for sudoku board."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        value: int = 0,
        font: Font | None = None,
    ) -> None:
        """Initialize the cell with its position and value."""
        if font is None:
            font = pygame.font.Font(pygame.font.get_default_font(), 36)
        super().__init__()
        self.x: int = x
        self.y: int = y
        self.value: int = value
        self.width: int = width
        self.height: int = height
        self.font = font

        # state
        self.locked = False
        self.valid = True
        self.reason = False
        self.highlight = True
        # self.hints = self.__create_hints(self.font)

        self.image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        _ = self.image.fill("white")

        self.rect = self.image.get_rect(topleft=(x, y))

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.value == other.value
        return self.value == other

    @override
    def __hash__(self) -> int:
        return super().__hash__()

    @override
    def __repr__(self):
        return f"Cell({self.value})@({self.x},{self.y})"

    @override
    def draw(self, screen: pygame.Surface) -> None:
        """Draw cell on the screen.

        draws the cell on the screen, with a magin around the board

        Args:
            screen: game window
        """
        if self.reason:
            fill_color = "yellow"
        elif self.selected or self.highlight:
            fill_color = "light grey"
        else:
            fill_color = "white"

        _ = self.image.fill(fill_color)
        _ = screen.blit(self.image, self.rect)
        _ = pygame.draw.rect(screen, "grey", self.rect, width=3)

        if self.locked:
            color = LOCK_COLOR
        elif not self.valid:
            color = INVALID_COLOR
        else:
            color = USER_COLOR

        text_surf = self.font.render(
            str(self.value if self.value not in (0, None) else ""),
            True,  # noqa: FBT003
            color,
        )
        # center it in the cell`s rect
        text_rect = text_surf.get_rect(center=self.rect.center)
        _ = screen.blit(text_surf, text_rect)

    @override
    def update(self, value: int) -> None:
        """Update the value of the cell.

        Args:
            value: new value
        """
        self.value = value

    @override
    def select(self) -> None:
        """Set selected to True."""
        if not self.locked:
            self.selected = True

    @override
    def unselect(self) -> None:
        """Set selected to False."""
        self.selected = False

    def lock(self):
        """Set pre-entered value as locked."""
        self.locked = True
