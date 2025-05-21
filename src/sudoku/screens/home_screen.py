"""Home screen for sudoku app."""

from typing import Any, final, override

import pygame
from pygame import Surface

from sudoku.screens.screen import Screen


@final
class HomeScreen(Screen):
    """Home screen class."""

    def __init__(self, window: Surface, name: str, resources: dict[str, Any] | None = None):
        """Constructor for play screen class.

        Args:
            window: surface to draw on
            name: name of screen
            resources: and relevant resources
        """
        super().__init__(window, name, resources)
        if resources is None:
            self.font = self.fonts["default"]
        else:
            self.font = self.fonts.get(resources.get("font", ""), self.fonts["default"])

    @override
    def enter(self, context: dict[str, Any]):
        pass

    @override
    def exit(self):
        # TODO(brinhasavlin): store game file
        pass

    @override
    def update(self, *args, **kwargs) -> None:
        pass

    @override
    def handle_events(self, events: list[pygame.event.Event]) -> list[str]:
        ret: list[str] = []
        return ret

    @override
    def draw(self) -> None:
        pass
