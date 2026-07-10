from PyQt6.QtWidgets import QApplication
from core.engine import Engine
from ui.main_window import MainWindow

import sys
import ctypes
import json
from pydantic import TypeAdapter, ValidationError
from dataclasses import asdict

import solutions
from models.game_settings import GameSettings

def main():
    settings = load_settings()

    myappid = "PySnake_v1.9"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    engine = Engine(settings)
    app = QApplication(sys.argv)
    window = MainWindow(engine, settings)
    window.show()
    sys.exit(app.exec())

def load_settings() -> GameSettings:
    try:
        with open("settings.json") as f:
            data = json.load(f)
        return TypeAdapter(GameSettings).validate_python(data)

    except FileNotFoundError:
        print("settings.json not found, creating default...")
    except json.JSONDecodeError as e:
        print(f"settings.json is corrupted ({e}), resetting to default...")
    except ValidationError as e:
        print(f"settings.json has invalid values ({e}), resetting to default...")

    default = GameSettings()
    with open("settings.json", "w") as f:
        json.dump(asdict(default), f, indent=4)
    return default

if __name__ == "__main__":
    main()