"""Button class."""

import logging
from typing import final, override

import pygame
from pygame.font import Font

from sudoku.constants import CELL_SIZE
from sudoku.game_sprites import GameSprite

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class Button(GameSprite):
    """Button Class."""

    def __init__(self, x: int, y: int, name: str, font: Font) -> None:
        """Construoctor for Button object.

        Places a clickable button

        Args:
            x: x position of button
            y: y position of button
            name: name of button
            font: font for button text
        """
        super().__init__()
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.font: Font = font
        self.image: pygame.Surface = pygame.Surface((CELL_SIZE * 9, CELL_SIZE * 9))
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))

    @override
    def update(self, *args, **kwargs) -> None:
        """Update the sprite."""
        logger.warning("buttons do not get updated")
        raise NotImplementedError

    @override
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the sprite on the screen."""
        _ = self.image.fill("white")
        _ = screen.blit(self.image, self.rect)
        _ = pygame.draw.rect(screen, "grey", self.rect, width=3)

        # if self.locked:
        text_surf = self.font.render(
            self.name,
            True,  # noqa: FBT003
            "black",
        )
        # center it in the cell`s rect
        text_rect = text_surf.get_rect(center=self.rect.center)
        _ = screen.blit(text_surf, text_rect)

    @override
    def select(self) -> None:
        """Select the sprite."""
        logger.info(f"{self.name} button has been pressed")
        self.selected: bool = True

    @override
    def unselect(self) -> None:
        """Unselect the sprite."""
        logger.warning("button selection is a one way function")
        raise NotImplementedError


@final
class Back(Button):
    """Back Button."""

    def __init__(self, font: Font) -> None:
        """Back Button.

        Args:
            font: font
        """
        super().__init__(200, 200, "home", font)
