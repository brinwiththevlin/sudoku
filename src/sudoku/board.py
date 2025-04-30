"""Board and Cell classes."""

from typing import final, override

import pygame
from pygame.font import Font

from sudoku.constants import CELL_SIZE
from sudoku.game_sprites import GameSprite
from sudoku.groups import drawable, selectable, updatable


@final
class Cell(GameSprite):
    """Cell class for sudoku board."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        value: int | None = None,
        font: Font | None = None,
    ) -> None:
        """Initialize the cell with its position and value."""
        if font is None:
            font = pygame.font.Font(pygame.font.get_default_font(), 36)
        super().__init__()
        updatable.add(self)
        selectable.add(self)
        self.x: int = x
        self.y: int = y
        self.value: int | None = value
        self.width: int = width
        self.height: int = height
        self.font = font
        self.locked = False

        self.image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        _ = self.image.fill("white")

        self.rect = self.image.get_rect(topleft=(x, y))

    @override
    def draw(self, screen: pygame.Surface) -> None:
        """Draw cell on the screen.

        draws the cell on the screen, with a magin around the board

        Args:
            screen: game window
        """
        color = (0, 0, 0) if self.locked else (0, 0, 200)
        _ = self.image.fill("light grey") if self.selected else self.image.fill("white")
        _ = screen.blit(self.image, self.rect)
        _ = pygame.draw.rect(screen, "grey", self.rect, width=3)
        text_surf = self.font.render(
            str(self.value if self.value not in (0, None) else ""), True, color  # noqa: FBT003
        )
        # center it in the cell`s rect
        text_rect = text_surf.get_rect(center=self.rect.center)
        _ = screen.blit(text_surf, text_rect)

    @override
    def update(self, value: int) -> None:
        """Update the value of the cell.

        Args:
            value: new value
        """
        self.value = value

    @override
    def select(self) -> None:
        """Set selected to True."""
        if not self.locked:
            self.selected = True

    @override
    def unselect(self) -> None:
        """Set selected to False."""
        self.selected = False

    def lock(self):
        """Set pre-entered value as locked."""
        self.locked = True


@final
class Board(GameSprite):
    """Board class."""

    def __init__(self, x: int, y: int) -> None:
        """Constructor for board class.

        Creates a sudoku board, 9 by 9

        Args:
            x: x position of top left corner
            y: y position of top left corner
        """
        super().__init__()
        drawable.add(self)
        self.x = x
        self.y = y
        self.image = pygame.Surface((CELL_SIZE * 9, CELL_SIZE * 9))
        _ = self.image.fill("white")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cells = self.__create_cells()

    @override
    def update(self) -> None:
        raise NotImplementedError

    @override
    def draw(self, screen: pygame.Surface) -> None:
        _ = screen.blit(self.image, self.rect)

        for row in self.cells:
            for cell in row:
                cell.draw(screen)

        _ = pygame.draw.rect(screen, "black", self.rect, width=3)
        for i in range(3, 9, 3):
            _ = pygame.draw.line(
                screen,
                "black",
                (self.x + i * CELL_SIZE, self.y),
                (self.x + i * CELL_SIZE, self.y + 9 * CELL_SIZE),
                width=3,
            )
            _ = pygame.draw.line(
                screen,
                "black",
                (self.x, self.y + i * CELL_SIZE),
                (self.x + 9 * CELL_SIZE, self.y + i * CELL_SIZE),
                width=3,
            )

    @override
    def select(self) -> None:
        raise NotImplementedError

    @override
    def unselect(self) -> None:
        raise NotImplementedError

    def __create_cells(self) -> list[list[Cell]]:
        cells: list[list[Cell]] = [
            [Cell(self.x + CELL_SIZE * col, self.y + CELL_SIZE * row, CELL_SIZE, CELL_SIZE) for col in range(9)]
            for row in range(9)
        ]
        return cells

    def load(self, values: list[str]) -> None:
        """Load a sudoku board from a 2D list of values.

        Args:
            values: 2D list of values empty values a represented by .
        """
        for i, line in enumerate(values):
            for j, v in enumerate(line.split()):
                if v.isnumeric():
                    self.cells[i][j].update(int(v))
                    self.cells[i][j].lock()
