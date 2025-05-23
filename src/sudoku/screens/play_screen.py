"""Play screen for sudoku app."""

import json
import logging
import sys
from pathlib import Path
from typing import Any, final, override

import pygame
from pygame import Surface, display

from sudoku.board import Board
from sudoku.button import Back
from sudoku.cell import Cell
from sudoku.constants import XMARGIN, YMARGIN
from sudoku.screens.screen import Screen, ScreenEvent

logger = logging.getLogger(__name__)


@final
class PlayScreen(Screen):
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
        self.board: Board = Board(XMARGIN, YMARGIN, self.font)
        self.back = Back(self.font)

        self.drawable.add(self.back)
        self.selectable.add(self.back)
        self.drawable.add(self.board)
        for cell in self.board:
            self.drawable.add(cell)
            self.selectable.add(cell)
            self.updatable.add(cell)

    @override
    def enter(self, context: dict[str, Any]):
        """Upon entering load the puzzle.

        Args:
            context: context needed to load puzzle

        Raises:
            ValueError: if the name is not valid don't load a puzzle.
        """
        self.data = context
        # if puzzle.txt exists at project root load it
        if type(self.data["file_name"]) is not str:
            raise ValueError("file_name, must be a string")
        if Path(self.data["file_name"]).exists():
            with Path(self.data["file_name"]).open() as f:
                puzzle = json.load(f)
                self.board.load(puzzle["current"])
        else:
            raise FileNotFoundError
        # set title of window
        display.set_caption(self.data["file_name"].removesuffix(".json"))

    @override
    def exit(self) -> None:
        """Exits the play screen. saves before exiting."""
        # TODO(brinhasavlin): store game file

        state = self.board.to_string()
        with Path.open(self.data["file_name"], mode="r") as f:
            data = json.load(f)
            data["current"] = state
        with Path.open(self.data["file_name"], mode="w") as f:
            logger.info(data)
            json.dump(data, f)

    @override
    def update(self, *args, **kwargs) -> None:
        pass

    @override
    def handle_events(self, events: list[pygame.event.Event]) -> ScreenEvent | None:
        """Handle all game events.

        Args:
            events: list of all pygame envents

        Returns:
            a screen change event or nothing.
        """
        # TODO(brinhasavlin): add more controls (i.e. annotation, multi select)
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
                            if type(s) is Cell:
                                self.board.highlight(s.value)
                            if type(s) is Back:
                                return ScreenEvent(self.back.name, {})
                            break
                    else:
                        self.board.highlight(0)
                case pygame.KEYDOWN:
                    if pygame.K_0 <= event.key <= pygame.K_9:
                        digit = event.key - pygame.K_0
                        for s in self.selectable:
                            if s.selected:
                                s.update(digit)
                    if event.key == pygame.K_BACKSPACE:
                        for s in self.selectable:
                            if s.selected:
                                s.update(0)
                case _:
                    pass
        return None

    @override
    def draw(self) -> None:
        """Draw everyting for this screen."""
        _ = self.window.fill("green" if self.board.solved(self.logger) else (200, 10, 50))
        self.back.draw(self.window)
        self.board.draw(self.window)
