from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QSlider, QPushButton, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from models.game_settings import GameSettings
import json
from pydantic import TypeAdapter
from dataclasses import asdict

class SettingsWindow(QWidget):
    settings_changed = pyqtSignal(GameSettings)
    game_speed_changed = pyqtSignal(int)

    def __init__(self, game):
        super().__init__()
        self._game = game

        self.setWindowTitle("Settings")
        self.resize(400, 350)
        
        self.settings_file = "settings.json"
        
        self.current_settings: GameSettings = self.load_settings()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # 1. Width
        self.width_input = QSpinBox()
        self.width_input.setRange(7, 50)
        self.width_input.setValue(int(self.current_settings.width))
        layout.addLayout(self.create_form_row("Width:", self.width_input))

        # 2. Height
        self.height_input = QSpinBox()
        self.height_input.setRange(7, 50)
        self.height_input.setValue(int(self.current_settings.height))
        layout.addLayout(self.create_form_row("Height:", self.height_input))

        # 3. Game Speed
        speed_label = QLabel("Game Speed:")
        layout.addWidget(speed_label)
        
        speed_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 200)
        
        self.speed_input = QSpinBox()
        self.speed_input.setRange(1, 200)
        self.speed_input.setFixedWidth(60)
        
        initial_speed = self.current_settings.game_speed
        self.speed_slider.setValue(initial_speed)
        self.speed_input.setValue(int(initial_speed))
        
        self.speed_slider.valueChanged.connect(self.sync_slider_to_input)
        self.speed_input.textChanged.connect(self.sync_input_to_slider)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_input)
        layout.addLayout(speed_layout)

        # 4. Seed
        self.random_seed_checkbox = QCheckBox("Random seed:")
        self.random_seed_checkbox.setChecked(self.current_settings.use_random_seed)

        self.seed_input = QLineEdit()
        self.seed_input.setValidator(QIntValidator())
        self.seed_input.setText(str(self.current_settings.seed))

        self.seed_input.setEnabled(not self.random_seed_checkbox.isChecked())
        self.random_seed_checkbox.toggled.connect(
            lambda checked: self.seed_input.setEnabled(not checked)
        )

        seed_layout = QHBoxLayout()
        seed_layout.addWidget(self.random_seed_checkbox)
        seed_layout.addWidget(self.seed_input)
        layout.addLayout(seed_layout)

        ####

        layout.addStretch()

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.save_settings)
        layout.addWidget(self.apply_button)

    def create_form_row(self, label_text, widget):
        """Helper method creating a horizontal layout: Label + Input widget"""

        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        return row_layout

    def load_settings(self):
        """Safe loading of JSON files, preventing crashes due to file structure errors."""

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return TypeAdapter(GameSettings).validate_python(json.load(f))
        except json.JSONDecodeError:
            pass

    def sync_slider_to_input(self, new_game_speed):
        """Updating the text field based on slider movement"""

        self.speed_input.blockSignals(True)
        self.speed_input.setValue(int(new_game_speed))
        self.speed_input.blockSignals(False)
        self.save_game_speed(new_game_speed)

    def sync_input_to_slider(self, text):
        """Updating the slider based on manually entered text"""

        if text:
            try:
                new_game_speed = int(text)
                if self.speed_slider.minimum() <= new_game_speed <= self.speed_slider.maximum():
                    self.speed_slider.blockSignals(True)
                    self.speed_slider.setValue(new_game_speed)
                    self.speed_slider.blockSignals(False)
                    self.save_game_speed(new_game_speed)
            except ValueError:
                pass

    def save_game_speed(self, new_game_speed: int):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                self.game_speed_changed.emit(new_game_speed)
                self.current_settings.game_speed = new_game_speed
                json.dump(asdict(self.current_settings), f, indent=4, ensure_ascii=False)

            print("Speed saved")
        except Exception as e:
            KeyError("Error while saving new game speed")


    def save_settings(self):
        """Data retrieval, final validation, and secure saving to the settings.json file."""

        try:
            updated_settings = GameSettings(
                width=self.width_input.value(),
                height=self.height_input.value(),
                game_speed=self.speed_input.value(),
                use_random_seed=self.random_seed_checkbox.isChecked(),
                seed=self.seed_input.text()
            )

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(asdict(updated_settings), f, indent=4, ensure_ascii=False)

            print("Applied")
            self.settings_changed.emit(updated_settings)
            self.current_settings = updated_settings
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while saving: {str(e)}")