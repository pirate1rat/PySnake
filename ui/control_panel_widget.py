from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

from core.engine import Engine
from models.game_state import GameState

class ControlPanelWidget(QWidget):
    def __init__(self, game: Engine, registry: list, import_solution):
        super().__init__()
        self._game = game

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- dropdown options ---
        self.combo = QComboBox()
        self.combo.addItems(registry)
        print(registry)
        self.combo.currentTextChanged.connect(import_solution)
        self.combo.setCurrentIndex(1)
        self.combo.setFixedWidth(160)

        main_layout.addWidget(self.combo)

        # --- buttons ---
        grid = QGridLayout()
        for i in range(4):
            grid.setColumnStretch(i, 0)
        # for i in range(2):
        #     grid.setRowStretch(i, 0)

        self.play_pause_btn = QPushButton()
        self.play_pause_btn.setFixedSize(64, 64)
        self.play_pause_btn.setIconSize(QSize(64, 64))
        self.play_pause_btn.setIcon(QIcon("ui/images/icons8-play-50.png"))
        self.play_pause_btn.clicked.connect(self._toggle_play_pause)

        self.restart_btn = QPushButton()
        self.restart_btn.setFixedSize(64, 64)
        self.restart_btn.setIconSize(QSize(64, 64))
        self.restart_btn.setIcon(QIcon("ui/images/icons8-restart-50.png"))
        self.restart_btn.clicked.connect(self._game.restart)

        self.loop_btn = QPushButton()
        self.loop_btn.setFixedSize(64, 64)
        self.loop_btn.setIconSize(QSize(64, 64))
        self.loop_btn.setIcon(QIcon("ui/images/icons8-loop-50.png"))
        self.loop_btn.clicked.connect(self._game.run_in_loop)

        # self.visible_btn = QPushButton()
        # self.visible_btn.setIcon(QIcon("images/visible.png"))
        # self.visible_btn.clicked.connect(self._game.toggle_visible)

        grid.addWidget(self.play_pause_btn, 0, 0)
        grid.setColumnMinimumWidth(0, 160)
        grid.addWidget(self.restart_btn, 0, 2)
        grid.addWidget(self.loop_btn, 0, 3)
        grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # grid.addWidget(self.visible_btn, 1, 1)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def _toggle_play_pause(self):
        if self._game._state == GameState.GAME_IS_PAUSED:
            self._game.resume()
            self.play_pause_btn.setIcon(QIcon("ui/images/icons8-pause-50.png"))
        else:
            self._game.pause()
            self.play_pause_btn.setIcon(QIcon("ui/images/icons8-play-50.png"))