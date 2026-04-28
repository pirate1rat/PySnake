from enum import Enum, auto

class Tile(Enum):
    BORDER = auto()
    EMPTY = auto()
    SNAKE = auto()
    APPLE = auto()