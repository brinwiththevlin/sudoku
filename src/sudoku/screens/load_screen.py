
"""Load screen for sudoku app."""

import json
import logging
import sys
from pathlib import Path
from typing import Any, final, override

import pygame
from pygame import Surface, display

from sudoku.button import Back, Button
from sudoku.constants import PUZZLE_DIR, SCREEN_WIDTH, CELL_SIZE, THUMB_DIR
from sudoku.screens.screen import Screen, ScreenEvent

logger = logging.getLogger(__name__)


@final
class LoadScreen(Screen):
    """Play screen class."""

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
        self.back = Back(self.font)
        self.page = 0
        self.thumbnails, self.buttons = self.load_page()

        self.drawable.add(self.back)
        self.selectable.add(self.back)
        for button in self.buttons:
            self.drawable.add(button)
            self.selectable.add(button)
        self.mode: str = ""

    @override
    def enter(self, context: dict[str, Any]):
        """Upon entering save the mode.

        Args:
             context: context needed to save mode
        """
        self.mode = context["mode"]
        display.set_caption("Pick a puzzle")

    @override
    def exit(self) -> None:
        """Exits the load screen. Saves before exiting."""
        self.updatable.empty()
        self.drawable.empty()
        self.selectable.empty()
        pass

    @override
    def update(self, *args, **kwargs) -> None:
        pass

    @override
    def handle_events(self, events: list[pygame.event.Event]) -> ScreenEvent | None:
        """Handle all game events.

        Args:
            events: list of all pygame events

        Returns:
            a screen change event or nothing.
        """
        for event in events:
            match event.type:
                case pygame.QUIT:
                    sys.exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    [s.unselect() for s in self.selectable]
                    for s in self.selectable:
                        if s.rect.collidepoint(*pos):
                            s.select()
                            if s is self.back:
                                return ScreenEvent(self.back.name, {})
                            else:
                                return ScreenEvent(self.mode, {"file_name": PUZZLE_DIR / (s.name + ".json")})
        return None

    @override
    def draw(self) -> None:
        """Draw everything for this screen."""
        _ = self.window.fill("white")
        self.back.draw(self.window)
        for i, button in enumerate(self.buttons):
            button.draw(self.window)
            if i < len(self.thumbnails) and self.thumbnails[i]:
                # Draw the thumbnail to the left of the button
                thumbnail = self.thumbnails[i]
                thumbnail = pygame.transform.scale(thumbnail, (400, 400))
                thumbnail_rect = thumbnail.get_rect()
                thumbnail_rect.midright = (button.rect.left - 10, button.rect.centery)
                self.window.blit(thumbnail, thumbnail_rect)

    def load_page(self) -> tuple[list[Surface],list[Button]]:
        """Loads the buttons for the page."""

        thumbnails = []
        buttons = []
        if hasattr(self, "buttons"):
            [button.kill() for button in self.buttons]
        count = 0
        for path_obj in PUZZLE_DIR.iterdir():
            if count // 3 < self.page:
                count += 1
                continue
            if count // 3 > self.page:
                break
            with open(str(path_obj), "r") as f:
                data = json.load(f)
                thumbnail_path = data.get("thumbnail")
                if thumbnail_path:
                    thumbnail_surface = pygame.image.load(str(THUMB_DIR / thumbnail_path)).convert_alpha()
                    thumbnails.append(thumbnail_surface)
                else:
                    thumbnails.append(None)
                buttons.append(Button(SCREEN_WIDTH//2 + CELL_SIZE  ,150 * (count + 1) , path_obj.name.removesuffix(".json"), self.font))
        return thumbnails, buttons
