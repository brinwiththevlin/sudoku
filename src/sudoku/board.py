"""Board class."""

import logging
from collections.abc import Generator
from typing import final, override

import pygame
from pygame.font import Font

from sudoku.cell import Cell
from sudoku.constants import CELL_SIZE
from sudoku.game_sprites import GameSprite


@final
class Board(GameSprite):
    """Board class."""

    def __init__(self, x: int, y: int, font: Font) -> None:
        """Constructor for board class.

        Creates a sudoku board, 9 by 9

        Args:
            x: x position of top left corner
            y: y position of top left corner
            font: text font for all cells
        """
        super().__init__()
        self.x = x
        self.y = y
        self.font = font
        self.image = pygame.Surface((CELL_SIZE * 9, CELL_SIZE * 9))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cells = self.__create_cells(font=font)

    def __iter__(self) -> Generator[Cell, None, None]:  # noqa: D105
        for row in self.cells:
            yield from row

    @override
    def update(self) -> None:
        raise NotImplementedError

    @override
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the whole board.

        Args:
            screen: screen to draw the board on.
        """
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

    def __create_cells(self, font: Font) -> list[list[Cell]]:
        cells: list[list[Cell]] = [
            [
                Cell(self.x + CELL_SIZE * col, self.y + CELL_SIZE * row, CELL_SIZE, CELL_SIZE, font=font)
                for col in range(9)
            ]
            for row in range(9)
        ]
        return cells

    def highlight(self, value: int) -> None:
        """Highlight all cells with the same value.

        Args:
            value: value to highlight
        """
        for row in self.cells:
            for cell in row:
                cell.highlight = value != 0 and cell.value == value

    def load(self, values: list[str]) -> None:
        """Load a sudoku board from a 2D list of values.

        Args:
            values: 2D list of values empty values a represented by .
        """
        for i, line in enumerate(values):
            for j, v in enumerate(line.split()):
                if v.isnumeric() or v.startswith("*"):
                    self.cells[i][j].update(int(v[-1]))
                    if v.startswith("*"):
                        self.cells[i][j].lock()

    def to_string(self) -> list[str]:
        """Converts board state to the strings that will be added to the json file.

        Returns:
            String representation of board state
        """
        rows: list[str] = []
        for row in self.cells:
            string = " ".join([f"{'*' if cell.locked else ''}{cell.value if cell.value != 0 else '.'}" for cell in row])
            rows.append(string)
        return rows

    def solved(self, logger: logging.Logger) -> bool:
        """Checks if board is solved.

        Returns:
            true if solved
        """
        for row in self.cells:
            for cell in row:
                cell.valid = True
                cell.reason = False
        fault = False
        block_sets: list[set[int]] = [set() for _ in range(9)]
        for i in range(9):
            row_set: set[int] = set()
            col_set: set[int] = set()

            for j in range(9):
                current_block: set[int] = block_sets[3 * (i // 3) + (j // 3)]
                if self.cells[i][j].value in row_set or self.cells[i][j].value in current_block:
                    fault = True
                    logger.debug(f"Invalid cell {i}, {j}")
                    self.invalidate(i, j)

                if self.cells[i][j].value != 0:
                    row_set.add(self.cells[i][j].value)
                    block_sets[3 * (i // 3) + (j // 3)].add(self.cells[i][j].value)

                if self.cells[j][i].value in col_set:
                    fault = True
                    self.invalidate(j, i)
                    logger.debug(f"Invalid cell {j}, {i}")

                if self.cells[j][i].value != 0:
                    col_set.add(self.cells[j][i].value)

            if len(row_set) != 9 or len(col_set) != 9:  # noqa: PLR2004
                fault = True

        return not any(len(s) != 9 for s in block_sets) and not fault  # noqa: PLR2004

    def invalidate(self, i: int, j: int) -> None:
        """Invalidate a cell and all cells with the same value.

        Args:
            i: row index
            j: column index
        """
        bad_val = self.cells[i][j].value
        if bad_val in (None, 0):
            return

        # Mark the original cell
        self.cells[i][j].valid = False
        self.cells[i][j].reason = True

        for r in range(9):
            for c in range(9):
                # skip the original
                if (r, c) == (i, j):
                    continue

                cell = self.cells[r][c]
                if cell.value != bad_val:
                    continue

                same_row = r == i
                same_col = c == j
                same_block = r // 3 == i // 3 and c // 3 == j // 3

                if same_row or same_col or same_block:
                    cell.valid = False
                    cell.reason = True

    def relocate(self, x: int, y: int) -> None:
        self.x = 0
        self.y = 0
        self.rect.topleft = (x, y)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].x = x + CELL_SIZE * i
                self.cells[i][j].y = y + CELL_SIZE * j
                self.cells[i][j].rect.topleft = (x + CELL_SIZE * i, y + CELL_SIZE * j)
