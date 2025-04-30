"""Sprite groups for the game."""

from typing import TYPE_CHECKING

from pygame.sprite import Group

if TYPE_CHECKING:
    from sudoku.game_sprites import GameSprite

drawable: "Group[GameSprite]" = Group()
updatable: "Group[GameSprite]" = Group()
selectable: "Group[GameSprite]" = Group()
