"""File containing constants for the game."""
from pathlib import Path

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
YMARGIN = 45
XMARGIN = 350

# cell
CELL_SIZE = 70
LOCK_COLOR = (0, 0, 0)
USER_COLOR = (0, 0, 200)
INVALID_COLOR = (255, 0, 0)

PUZZLE_DIR = Path(__file__).parent.parent.parent / "puzzles"
THUMB_DIR = Path(__file__).parent.parent.parent / "thumbnails"
