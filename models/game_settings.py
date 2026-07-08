from dataclasses import dataclass

@dataclass
class GameSettings:
    block_size: int #in pixels
    width: int = 10
    height: int = 10
    game_speed: int = 50
    use_random_seed: bool = True
    seed: str = "1337"