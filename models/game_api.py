from dataclasses import dataclass
from models.snake import Snake
from models.tiles import Tile
from utils.vector2 import vec2
from registry import register

@dataclass
class GameContext:
    board: list[list[int]]
    snake: Snake
    apple: vec2
    width: int
    height: int