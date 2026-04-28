from enum import Enum, auto

class GameState(Enum):
    GAME_IS_OVER = auto()
    GAME_IS_RUNNING = auto()
    GAME_IS_PAUSED = auto()
    GAME_SET_READY = auto()