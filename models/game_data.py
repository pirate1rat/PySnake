from dataclasses import dataclass, fields

@dataclass
class GameStatistics:
    points: int = 0
    turns: int = 0
    measured_time: int = 0