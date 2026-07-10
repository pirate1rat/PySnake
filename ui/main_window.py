from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication
from PyQt6.QtGui import QGuiApplication, QAction, QIcon
from PyQt6.QtCore import QTimer, Qt

from ui.board_widget import BoardWidget
from ui.control_panel_widget import ControlPanelWidget
from ui.chart_widget import ChartWidget
from ui.console_widget import ConsoleWidget
from ui.settings_window import SettingsWindow

from registry import *

from core.engine import Engine
from models.game_settings import GameSettings
from models.game_state import *
from models.tiles import *

import importlib


class MainWindow(QMainWindow):
    def __init__(self, game: Engine, settings: GameSettings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle("PySnake")
        self.resize(1050, 950)
        self.center()
        self.setWindowIcon(QIcon("ui/images/icons8-snake-64.ico"))

        self._game = game
        self._game.game_state_changed.connect(self.on_state_changed)

        self._chart_widget = ChartWidget(self._game)
        self._console_widget = ConsoleWidget(self._game)
        self._board_widget = BoardWidget(self._game.get_board())
        self._control_panel = ControlPanelWidget(self._game, get_registry_str(), self.import_solution)

        central = QWidget()
        main_layout = QHBoxLayout(central)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        menu_bar = self.menuBar()

        left_layout.addWidget(self._board_widget, alignment=Qt.AlignmentFlag.AlignCenter)
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

        settings_menu = menu_bar.addMenu("Settings")
        setting_action = QAction("Parameters", self)
        setting_action.triggered.connect(self.open_parameters_window)
        settings_menu.addAction(setting_action)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(self.settings.game_speed)  # ms

    def import_solution(self, module_class_name):
        print(f"chosen: {module_class_name}")
        self._game.initialize_solution(get_registry()[module_class_name])
        self._console_widget.module_name = module_class_name
        self._chart_widget.settings = self.settings
        self._chart_widget.module_name = module_class_name
        self.apply_new_settings(self.settings)

    def update_game(self):
        self._game.update_game()
        self._board_widget.update()


    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())
    

    def on_state_changed(self, state):
        match state:
            case GameState.GAME_IS_PAUSED:
                print("game paused")
            case GameState.GAME_IS_RUNNING:
                print("game running")
            case GameState.GAME_IS_OVER:
                print("game ended")
            case GameState.GAME_SET_READY:
                self._board_widget.update()
                print("game restarted")


    def open_parameters_window(self):
        self.settings_window = SettingsWindow(self._game)
        self.settings_window.settings_changed.connect(self.apply_new_settings)
        self.settings_window.game_speed_changed.connect(self.change_game_speed)
        self.settings_window.show()
    

    def apply_new_settings(self, new_settings: GameSettings):
        self.settings = new_settings
        self._game.initialize(self.settings)

        # passing new board to board_widget
        self._board_widget.initialize(self._game.get_board())
    
    def change_game_speed(self, new_game_speed: int):
        self.settings.game_speed = new_game_speed
        self.timer.start(self.settings.game_speed)

    def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()
