from dataclasses import dataclass, fields

@dataclass
class GameStatistics:
    points: int = 0
    turns: int = 0
    compute_time_sum: float = 0