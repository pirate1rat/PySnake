from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLabel
from PyQt6.QtCore import Qt

from game_logic.game import Game
from game_logic.utils.gamedata import GameStatistics
from dataclasses import fields

import numpy as np

class ConsoleWidget(QWidget):
    def __init__(self, game: Game):
        super().__init__()
        self._game = game
        self._game.return_statistics.connect(self.add_to_history)
        
        self.keys = [f.name for f in fields(GameStatistics)]
        self.history = {key: [] for key in self.keys}

        self.num_of_games: int = 0

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Last games:"))
        self._last_games_console = QPlainTextEdit()
        self._last_games_console.setReadOnly(True)
        self._last_games_console.setStyleSheet("font-family: 'Consolas', 'Monospace'; background-color: #f0f0f0;")
        layout.addWidget(self._last_games_console)

        layout.addWidget(QLabel("Average statistics:"))
        self._averages_console = QPlainTextEdit()
        self._averages_console.setReadOnly(True)
        self._averages_console.setMaximumHeight(150)
        self._averages_console.setStyleSheet("font-family: 'Consolas', 'Monospace';")
        layout.addWidget(self._averages_console)

        self._log_history = []

    def add_to_history(self, stats):
        """Takes set of data from ended game and adds to history"""

        self.num_of_games += 1

        for key in self.keys:
            val = getattr(stats, key, 0)
            self.history[key].append(val)
        
        self.update_consoles()

    def update_consoles(self):
        """
        Updates console based on history of games.
        history: dict { 'stat_name': [values] }
        """

        max_lines = 10
        
        if self.num_of_games == 0:
            self._last_games_console.clear()
            self._averages_console.clear()
            self._log_history = []
            return

        try:
            points = self.history.get('points', [0])[-1]
            turns = self.history.get('turns', [0])[-1]
            total_time = self.history.get('times', [0])[-1] 
            
            new_line = f"Game #{self.num_of_games}: points = {points}, turns = {turns}, time = {total_time}s"
            
            self._log_history.insert(0, new_line)
            self._log_history = self._log_history[:max_lines]
            
            self._last_games_console.setPlainText("\n".join(self._log_history))
        except (IndexError, KeyError) as e:
            print(f"Błąd podczas formatowania logu: {e}")

        self._averages_console.clear()
        avg_text = []
        for key, values in self.history.items():
            if values:
                mean_val = np.mean(values)
                avg_text.append(f"avg {key}: {mean_val:.2f}")
        
        self._averages_console.setPlainText("\n".join(avg_text))