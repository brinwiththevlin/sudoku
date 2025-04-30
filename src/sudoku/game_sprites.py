"""Abstract class for grouping."""

from abc import ABC, abstractmethod
from typing import override

import pygame


class GameSprite(pygame.sprite.Sprite, ABC):
    """Abstract class for grouping."""

    image: pygame.Surface
    rect: pygame.Rect
    selected: bool

    @abstractmethod
    def __init__(self, *groups) -> None:
        """Initialize the sprite."""
        super().__init__(*groups)
        self.selected = False

    @abstractmethod
    @override
    def update(self, *args, **kwargs) -> None:
        """Update the sprite."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the sprite on the screen."""
        raise NotImplementedError

    @abstractmethod
    def select(self) -> None:
        """Select the sprite."""
        raise NotImplementedError

    @abstractmethod
    def unselect(self) -> None:
        """Unselect the sprite."""
        raise NotImplementedError
