"""Screen manager module. to manage all screens."""

from typing import Any

import pygame
from pygame import Surface

from sudoku.screens.screen import Screen


class ScreenManager:
    """Screen manager module. to manage all screens."""

    def __init__(self, window: Surface) -> None:
        """Initialize the screen manager."""
        self.screens: dict[str, Screen] = {}
        self.active_screen: Screen | None = None
        self.window: Surface = window
        self.background: pygame.Color = pygame.Color("black")
        self.resources: dict[str, Any] = {}

    def register_screen(self, name: str, interface: type[Screen]) -> None:
        """Adds new screen to screens dictionary.

        Args:
            name: name of new screen
            interface: Screen object

        Raises:
            KeyError: raises error if name already  exists
        """
        if name in self.screens:
            raise KeyError("named window already exists")

        self.screens[name] = interface(self.window, name, self.resources)

    def switch_to(self, name: str, context: dict[str, Any]) -> None:
        """Switches manager to new active screen.

        Args:
            name: name of screen to switch too.
            context: any context that screen might need

        Raises:
            KeyError: fails if the screen to swith too does not exist.
        """
        if self.active_screen is not None:
            self.active_screen.exit()
        if name not in self.screens:
            raise KeyError(f"Screen {name} does not exist")

        self.active_screen = self.screens[name]
        self.active_screen.enter(context)

    def handle_events(self) -> None:
        """Handles events for the active screen.

        Raises:
            AttributeError: crashes if there is no active screen
        """
        evt = pygame.event.get()
        if self.active_screen is None:
            raise AttributeError("there is no active screen")
        manager_events = self.active_screen.handle_events(evt)
        for me in manager_events:
            if me in self.screens:
                self.switch_to(me, {})

    def update(self, dt: int) -> None:
        """Update everything on the new screen.

        Raises:
            AttributeError: crashes if there is no active screen
        """
        if self.active_screen is None:
            raise AttributeError("there is no active screen")
        self.active_screen.update(dt)

    def draw(self) -> None:
        """Draw to the active screen.

        Raises:
            AttributeError: crashes if there is no active screen
        """
        if self.active_screen is None:
            raise AttributeError("there is no active screen")
        self.active_screen.draw()
