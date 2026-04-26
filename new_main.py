from PyQt6.QtWidgets import QApplication
from game_logic.game import Game
from gui.main_window import MainWindow
import sys
import solutions

def main():
    snake = Game()
    app = QApplication(sys.argv)
    window = MainWindow(snake)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()