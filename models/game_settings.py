from dataclasses import dataclass

@dataclass
class GameSettings:
    block_size: int #in pixels
    width: int
    height: int
    game_speed: int