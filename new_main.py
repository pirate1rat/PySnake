from PyQt6.QtWidgets import QApplication
from game_logic.game import Game
from gui.main_window import MainWindow
import sys


def main():
    snake = Game()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()