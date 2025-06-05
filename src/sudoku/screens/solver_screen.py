"""Solver Screen."""

import json
import logging
import sys
from pathlib import Path
from typing import Any, final, override

import pygame
from pygame import Surface, display

from sudoku.board import Board
from sudoku.button import Back, Button
from sudoku.cell import Cell
from sudoku.constants import THUMB_DIR, XMARGIN, YMARGIN
from sudoku.screens.screen import Screen, ScreenEvent

logger = logging.getLogger(__name__)


@final
class SolverScreen(Screen):
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
        self.reset = Button(self.back.x, self.back.y + self.back.rect.height, "reset", self.font)
        self.file_name = ""

        self.drawable.add(self.back)
        self.selectable.add(self.back)
        self.drawable.add(self.reset)
        self.selectable.add(self.reset)
        self.drawable.add(self.board)
        for cell in self.board:
            self.drawable.add(cell)
            self.selectable.add(cell)
            self.updatable.add(cell)

    @override
    def enter(self, context: dict[str, Any]):
        """Upon entering, load the puzzle.

        Args:
            context: context needed to load puzzle

        Raises:
            ValueError: if the name is not valid, don't load a puzzle.
        """
        self.data = context
        # if puzzle.txt exists at the project root, load it
        if Path(self.data["file_name"]).exists():
            with Path(self.data["file_name"]).open() as f:
                puzzle = json.load(f)
                self.board.load(puzzle.get("current", puzzle["original"]))
        else:
            raise FileNotFoundError
        # set the title of the window
        self.file_name = Path(self.data["file_name"])
        display.set_caption(self.file_name.name.removesuffix(".json"))

    @override
    def exit(self) -> None:
        """Exits the play screen. Saves before exiting."""
        self.updatable.empty()
        self.drawable.empty()
        self.selectable.empty()

        state = self.board.to_string()
        thumbnail_path = THUMB_DIR / self.data["file_name"].name.replace(".json", ".png")
        with self.data["file_name"].open(mode="r") as f:  # Changed from Path.open to instance method
            data = json.load(f)
            data["current"] = state
            data["thumbnail"] = str(thumbnail_path)  # Convert Path to string for JSON

        # Write updated data
        with self.data["file_name"].open(mode="w") as f:  # Changed from Path.open to instance method
            logger.info(data)
            json.dump(data, f)

        # Save thumbnail in binary mode
        thumb_surface = pygame.Surface((self.board.rect.width, self.board.rect.height))
        _ = thumb_surface.fill("white")
        self.board.relocate(0, 0)
        self.board.draw(thumb_surface)
        pygame.image.save(thumb_surface, str(thumbnail_path))

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
                    with Path.open(self.data["file_name"], mode="r") as f:
                        data = json.load(f)
                        data["current"] = self.board.to_string()
                    with Path.open(self.data["file_name"], mode="w") as f:
                        logger.info(data)
                        json.dump(data, f)
                    sys.exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    [s.unselect() for s in self.selectable]
                    for s in self.selectable:
                        if s.rect.collidepoint(*pos):
                            s.select()
                            if type(s) is Cell:
                                self.board.highlight(s.value)
                            elif type(s) is Back:
                                return ScreenEvent(self.back.name, {})
                            elif type(s) is Button and s.name == "reset":
                                self.reset_board()
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
        """Draw everything for this screen."""
        _ = self.window.fill("green" if self.board.solved(self.logger) else (200, 10, 50))
        for d in self.drawable:
            if d is not self.board:
                d.draw(self.window)
        # self.back.draw(self.window)
        self.board.draw(self.window)

    def reset_board(self) -> None:
        """Reset the board so that any user entries are wiped.

        reseting is one directional, this can not be reversed
        """
        for cell in self.board:
            if not cell.locked:
                cell.value = 0
