from dataclasses import dataclass
from models.snake import Snake
from utils.vector2 import vec2

class GameContext:
    board: list[list[int]]
    snake: Snake
    apple: vec2
    width: int
    height: int


from enum import Enum, auto

class Direction (Enum):
    LEFT = auto()
    RIGT = auto()
    UP = auto()
    DOWN = auto()


from models.tiles import Tile
from registry import register