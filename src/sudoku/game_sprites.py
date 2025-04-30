"""Abstract class for grouping."""

from abc import ABC, abstractmethod
from typing import override

import pygame


class GameSprite(pygame.sprite.Sprite, ABC):
    """Abstract class for grouping."""

    image: pygame.Surface
    rect: pygame.Rect

    @abstractmethod
    @override
    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
