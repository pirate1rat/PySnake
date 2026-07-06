from PyQt6.QtWidgets import QApplication
from core.engine import Engine
from ui.main_window import MainWindow
import sys
import solutions

from models.game_settings import GameSettings
import json
from pydantic import TypeAdapter

def main():
    with open("settings.json") as f:
        data = json.load(f)
    settings = TypeAdapter(GameSettings).validate_python(data)

    engine = Engine(settings)
    app = QApplication(sys.argv)
    window = MainWindow(engine, settings)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()