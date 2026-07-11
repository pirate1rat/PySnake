## 🐍 Snake Algorithm Visualizer

A desktop app for visualizing and benchmarking Snake-playing algorithms. Built with Python and PyQt6.

---

## Screenshots
<img width="1038" height="970" alt="main" src="https://github.com/user-attachments/assets/f2e35a6c-8a09-4289-897b-f16ef3e7e6a2" />
<img width="390" height="375" alt="settings" src="https://github.com/user-attachments/assets/45528ee0-6743-4c71-b067-f969d8b6afb2" />

<!-- ![Main window](screenshots/main.png) -->
<!-- ![Settings](screenshots/settings.png) -->
---

## Features

- **Live visualization** of the snake game with adjustable speed
- **Play / Pause / Loop** simulation controls
- **Plugin-based architecture** — drop in your own algorithm in minutes
- **Statistics** — per-game and averaged results (points, turns, compute time)
- **Two charts** with selectable metrics
- **Mini console** showing last 30 games
- **CSV export** of full game history with run settings
- **Human player** — play yourself with WASD / arrow keys
- Configurable map size and random seed

## Built-in solutions

| Algorithm | Description |
|---|---|
| `HamComplete` | Full Hamiltonian cycle |
| `HamShort` | Hamiltonian cycle with shortcuts |
| `BFS` | Breadth-first search to apple |
| `MultiBFS` | BFS recalculated every step |
| `Human` | Manual keyboard control |

---

## Requirements

- Python 3.10+
- PyQt6
- pandas
- pydantic
- matplotlib

Install with:

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

---

## Writing your own solution

1. Copy `solution_template.py` into the `solutions/` folder
2. Uncomment `@register` and rename the class
3. Add the class name to `solutions/__init__.py`

```python
from models.game_api import GameContext, Tile, Snake, vec2, register

@register
class MySolution():
    def __init__(self, ctx: GameContext):
        pass  # called once at the start of each game

    def get_move(self, ctx: GameContext) -> vec2:
        pass  # return a vec2 direction each tick
              # e.g. vec2(1, 0) = right, vec2(0, -1) = up
```

`GameContext` gives you access to the board state, snake position and direction, apple position, and map dimensions.

---

## Project structure

```
├── core/           # game engine
├── models/         # data models and public API
├── solutions/      # algorithm plugins
├── ui/             # PyQt6 widgets
├── utils/          # helpers (vector2, registry)
├── main.py
├── settings.json   # persisted settings
└── solution_template.py
```
