from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer

from ui.board_widget import BoardWidget
from ui.control_panel import ControlPanel
from ui.chart_widget import ChartWidget
from ui.console_widget import ConsoleWidget

from config import *

from core.engine import Game
from models.game_state import *
from models.tiles import *

import importlib


class MainWindow(QMainWindow):
    def __init__(self, game: Game):
        super().__init__()
        self.setWindowTitle("PySnake")
        self.resize(1050, 950)
        self.center()
        #self.setWindowIcon(QIcon(""))

        self._game = game
        self._game.game_state_changed.connect(self.on_state_changed)

        self._board_widget = BoardWidget(self._game.board, BLOCK_SIZE)
        self._control_panel = ControlPanel(self._game, get_registry(), self.import_solution)
        self._chart_widget = ChartWidget(self._game)
        self._console_widget = ConsoleWidget(self._game)

        central = QWidget()
        main_layout = QHBoxLayout(central)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self._board_widget)
        left_layout.addWidget(self._control_panel)
        left_layout.addWidget(self._console_widget)
        right_layout.addWidget(self._chart_widget)

        central.setLayout(main_layout)
        self.setCentralWidget(central)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        #main_layout.addLayout(right_layout)

        # central.setLayout(layout)
        # self.setCentralWidget(central)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(GAME_SPEED)  # ms

    def import_solution(self, module_name):
        print(f"chosen: {module_name}")
        try:
            self.module = importlib.import_module(f"solutions.{module_name}")
        except ImportError as e:
            print(f"Unable to load {f"solutions.{module_name}"}", e)

    def update_game(self):
        # if self.my_game.GAME_RUNNING:
        #     parameters = self.my_game.update_game(self.module)
        #     if self.VISIBLE:
        #         self.update_canv(self.snake_canv, self.squares, self.my_game.conv_to_rgb())
        #     if parameters:
        #         self.statistics(parameters)

        # self.main_window.after(GAME_SPEED, self.update_game)
        self._game.update_game(self.module)
        self._board_widget.update()


    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())
    

    def on_state_changed(self, state):
        match state:
            case GameState.GAME_IS_PAUSED:
                print("gra zapauzowana")
            case GameState.GAME_IS_RUNNING:
                print("gra uruchomiona")
            case GameState.GAME_IS_OVER:
                print("gra zakończona")
            case GameState.GAME_SET_READY:
                self._board_widget.update()
                print("gra zrestartowana")

        
    # def game_running(self):
    #     self._game.resume()
    # def game_paused(self):
    #     self._game.pause()
    # def restart(self):
    #     self._game.restart()
    #     self.update_canv(self.snake_canv, self.squares, self._game.conv_to_rgb())
    # def game_inloop(self):
    #     self._game.in_loop()
    # def game_visible(self):
    #     self.VISIBLE = not self.VISIBLE