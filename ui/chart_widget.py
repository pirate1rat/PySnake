from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QFileDialog
from PyQt6.QtCore import QSize, Qt

from core.engine import Game
from models.game_data import GameStatistics

import numpy as np
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dataclasses import fields

class Chart:
    def __init__(self, color):
        self.fig = Figure(figsize=(6, 3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.color = color

class ChartWidget(QWidget):
    def __init__(self, game: Game):
        super().__init__()

        self._game = game
        self._game.return_statistics.connect(self.got_stats)

        self.keys = [f.name for f in fields(GameStatistics)]
        self.history = {key: [] for key in self.keys}
        self.num_of_games = 0

        self.stat_cv1 = Chart("black")
        self.stat_cv2 = Chart("blue")

        main = QVBoxLayout(self)

        # --- dropdown selection ---
        select_layout = QHBoxLayout()
        
        self.chart1_box = QComboBox()
        self.chart1_box.addItems(self.keys)
        if self.keys:
            self.chart1_box.setCurrentText(self.keys[0])
        self.chart1_box.currentTextChanged.connect(self.refresh_chart1)

        self.chart2_box = QComboBox()
        self.chart2_box.addItems(self.keys)
        if len(self.keys) > 1:
            self.chart2_box.setCurrentText(self.keys[1])
        self.chart2_box.currentTextChanged.connect(self.refresh_chart2)

        select_layout.addWidget(self.chart1_box)
        select_layout.addWidget(self.chart2_box)

        # --- buttons ---
        buttons_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("clear data")
        self.clear_btn.clicked.connect(self.clear_data)

        self.save_btn = QPushButton("save data")
        self.save_btn.clicked.connect(self.save_data)

        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.save_btn)

        #----------------------------------
        main.addLayout(select_layout)
        main.addWidget(self.stat_cv1.canvas)
        main.addWidget(self.stat_cv2.canvas)
        main.addLayout(buttons_layout)

        self.refresh_chart1()
        self.refresh_chart2()

    def got_stats(self, stats: GameStatistics):
        """Takes set of data from ended game and adds to history"""

        self.num_of_games += 1
        
        for key in self.keys:
            val = getattr(stats, key, 0)
            self.history[key].append(val)

        self.refresh_chart1()
        self.refresh_chart2()

    def refresh_chart1(self, *_):
        """Retrieve currently selected key and displays first chart"""

        selected_stat = self.chart1_box.currentText()
        if selected_stat in self.history:
            self.update_chart(self.stat_cv1, self.history[selected_stat], selected_stat)

    def refresh_chart2(self, *_):
        """Retrieve currently selected key and displays second chart"""

        selected_stat = self.chart2_box.currentText()
        if selected_stat in self.history:
            self.update_chart(self.stat_cv2, self.history[selected_stat], selected_stat)

    def update_chart(self, chart: Chart, datay, title: str):
        """Main logic to draw charts"""

        chart.ax.clear()
        
        datax = range(1, len(datay) + 1)

        if len(datay) > 0:
            chart.ax.plot(datax, datay, color=chart.color, marker='o')
            mean = np.mean(datay)
            chart.ax.axhline(mean, linestyle='--', label=f'avg = {mean:.2f}')
            chart.ax.legend()
        else:
            chart.ax.set_xlim(0, 1)
            chart.ax.set_ylim(0, 1)

        chart.ax.set_xlabel("Number of games")
        chart.ax.set_ylabel("Result")
        chart.ax.set_title(title)
        
        chart.canvas.draw_idle()

    def clear_data(self):
        """Clears history and refreshes charts"""

        self.num_of_games = 0
        self.history = {key: [] for key in self.keys}
        self.refresh_chart1()
        self.refresh_chart2()
    
    def save_data(self):
        """Saves data to .csv file"""
        
        if self.num_of_games == 0:
            print("No data to save")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save as",
            "",
            "CSV files (*.csv);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith('.csv'):
                file_path += '.csv'
                
            df = pd.DataFrame(self.history)
            
            df.to_csv(file_path, index=False, sep=';')
            print(f"History of {self.num_of_games} games successfully save to file {file_path}")