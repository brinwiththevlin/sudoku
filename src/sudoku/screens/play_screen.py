"""Play screen for sudoku app."""

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
        self.data = context
        # if puzzle.txt exists at project root load it
        if type(self.data["file_name"]) is not str:
            raise ValueError("file_name, must be a string")
        if Path(self.data["file_name"]).exists():
            with Path(self.data["file_name"]).open() as f:
                lines = f.readlines()
                self.board.load(lines)
        # set title of window
        display.set_caption(self.data["file_name"].removesuffix(".txt"))

    @override
    def exit(self) -> ScreenEvent:
        # TODO(brinhasavlin): store game file
        return ScreenEvent(self.back.name, {})

    @override
    def update(self, *args, **kwargs) -> None:
        pass

    @override
    def handle_events(self, events: list[pygame.event.Event]) -> ScreenEvent | None:
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
                                return self.exit()
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
        _ = self.window.fill("green" if self.board.solved(self.logger) else (200, 10, 50))
        self.back.draw(self.window)
        self.board.draw(self.window)
