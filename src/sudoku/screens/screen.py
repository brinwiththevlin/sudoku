"""Base class for all screens."""

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group

if TYPE_CHECKING:
    from sudoku.game_sprites import GameSprite


class ScreenEvent:
    """Data class tochange of screen events."""

    def __init__(self, screen: str, context: dict[str, Any]) -> None:
        """Screen change event.

        Args:
            screen: next screen name
            context: context to pass to the next screen
        """
        self.next_screen: str = screen
        self.context: dict[str, Any] = context


class Screen(ABC):
    """Base class for all game screens."""

    def __init__(self, window: Surface, name: str, resources: dict[str, Any] | None = None):
        """Initialize the screen.

        Args:
            window:  the main pygame display Surface
            name:    unique screen ID ("Home", "Play", "Solver")
            resources: optional dict of preloaded Surfaces, sounds, etc.
        """
        self.window: Surface = window  # pygame.Surface
        self.name: str = name
        self.rect: Rect = window.get_rect()  # pygame.Rect for layout
        self.resources: dict[str, Any] = resources if resources is not None else {}

        # lifecycle flags & payload
        self.active: bool = False
        self.data: Any = None  # passed into enter()

        # drawing & updates
        self.background: pygame.Color = pygame.Color("black")
        self.drawable: Group[GameSprite] = Group()
        self.updatable: Group[GameSprite] = Group()
        self.selectable: Group[GameSprite] = Group()

        # fonts
        self.fonts: dict[str, pygame.font.Font] = {
            "default": pygame.font.Font(None, 36),
        }
        self.logger: logging.Logger = logging.getLogger(__name__)

    @abstractmethod
    def enter(self, context: Any) -> None:
        """Called upon entering a new screen with context from previous screen.

        context can be anything

        Args:
            context: context from previous screen
        """
        raise NotImplementedError

    @abstractmethod
    def exit(self) -> ScreenEvent:
        """Called upon leaving a screen."""
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> ScreenEvent | None:
        """Handles all events on the screen."""
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Update the state of the data."""
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        """Draw state onto the surface."""
        raise NotImplementedError
