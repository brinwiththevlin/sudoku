"""Home screen for sudoku app."""

import logging
import sys
from typing import Any, final, override

import pygame
from pygame import Surface, display

from sudoku.button import Button
from sudoku.constants import CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from sudoku.screens.screen import Screen, ScreenEvent

logger = logging.getLogger(__name__)


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
        self.buttons: list[Button] = [
            Button(SCREEN_WIDTH // 2 - CELL_SIZE, SCREEN_HEIGHT - 600, "play", self.font),
            Button(SCREEN_WIDTH // 2 - CELL_SIZE, SCREEN_HEIGHT - 400, "solver", self.font),
            Button(SCREEN_WIDTH // 2 - CELL_SIZE, SCREEN_HEIGHT - 200, "builder", self.font),
        ]
        self.drawable.add(*self.buttons)
        self.selectable.add(*self.buttons)

    @override
    def enter(self, context: dict[str, Any]):
        display.set_caption("Sudoku game!")

    @override
    def exit(self) -> None:
        self.updatable.empty()
        self.drawable.empty()
        self.selectable.empty()
        logger.info(msg="leaving the main menu")
        name = ""
        for b in self.buttons:
            if b.selected:
                name = b.name
        if name == "":
            raise NameError("Invalid exit")

    @override
    def update(self, *args, **kwargs) -> None:
        """Nothing to update."""
        return

    @override
    def handle_events(self, events: list[pygame.event.Event]) -> ScreenEvent | None:
        for event in events:
            match event.type:
                case pygame.QUIT:
                    sys.exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for s in self.selectable:
                        if s.rect.collidepoint(*pos):
                            s.select()
                            if type(s) is Button:
                                return ScreenEvent("load", {"mode": s.name})
                case _:
                    pass
        return None

    @override
    def draw(self) -> None:
        _ = self.window.fill("white")
        for b in self.buttons:
            b.draw(self.window)
