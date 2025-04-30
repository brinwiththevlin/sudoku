"""Sprite groups for the game."""

from pygame.sprite import Group

from sudoku.game_sprites import GameSprite

# use Group[GameSprite], not AbstractGroup
drawable: Group[GameSprite] = Group()
updatable: Group[GameSprite] = Group()
