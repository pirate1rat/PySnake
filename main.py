from PyQt6.QtWidgets import QApplication
from core.engine import Game
from ui.main_window import MainWindow
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