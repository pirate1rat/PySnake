from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QSlider, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from models.game_settings import GameSettings
import json
from pydantic import TypeAdapter
from dataclasses import asdict

class SettingsWindow(QWidget):
    settings_changed = pyqtSignal(GameSettings)

    def __init__(self, game):
        super().__init__()
        self._game = game

        self.setWindowTitle("Settings")
        self.resize(400, 350)
        
        self.settings_file = "settings.json"
        
        self.current_settings: GameSettings = self.load_settings()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # 0. Block size
        self.block_size_input = QLineEdit()
        self.block_size_input.setValidator(QIntValidator(10, 50))
        self.block_size_input.setText(str(self.current_settings.block_size))
        layout.addLayout(self.create_form_row("Block Size:", self.block_size_input))

        # 1. Width
        self.width_input = QLineEdit()
        self.width_input.setValidator(QIntValidator(7, 30))
        self.width_input.setText(str(self.current_settings.width))
        layout.addLayout(self.create_form_row("Width:", self.width_input))

        # 2. Height
        self.height_input = QLineEdit()
        self.height_input.setValidator(QIntValidator(7, 30))
        self.height_input.setText(str(self.current_settings.height))
        layout.addLayout(self.create_form_row("Height:", self.height_input))

        # 3. Game Speed
        speed_label = QLabel("Game Speed:")
        layout.addWidget(speed_label)
        
        speed_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 200)
        
        self.speed_input = QLineEdit()
        self.speed_input.setValidator(QIntValidator(1, 200))
        self.speed_input.setFixedWidth(60)
        
        initial_speed = self.current_settings.game_speed
        self.speed_slider.setValue(initial_speed)
        self.speed_input.setText(str(initial_speed))
        
        self.speed_slider.valueChanged.connect(self.sync_slider_to_input)
        self.speed_input.textChanged.connect(self.sync_input_to_slider)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_input)
        layout.addLayout(speed_layout)

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

    def sync_slider_to_input(self, value):
        """Updating the text field based on slider movement"""

        self.speed_input.blockSignals(True)
        self.speed_input.setText(str(value))
        self.speed_input.blockSignals(False)

    def sync_input_to_slider(self, text):
        """Updating the slider based on manually entered text"""

        if text:
            try:
                value = int(text)
                if self.speed_slider.minimum() <= value <= self.speed_slider.maximum():
                    self.speed_slider.blockSignals(True)
                    self.speed_slider.setValue(value)
                    self.speed_slider.blockSignals(False)
            except ValueError:
                pass

    def save_settings(self):
        """Data retrieval, final validation, and secure saving to the settings.json file."""

        if not self.block_size_input.text() or not self.width_input.text() or not self.height_input.text() or not self.speed_input.text():
            QMessageBox.warning(self, "Validation Error", "All fields must be filled!")
            return

        try:
            updated_settings = GameSettings(
                block_size=int(self.block_size_input.text()),
                width=int(self.width_input.text()),
                height=int(self.height_input.text()),
                game_speed=int(self.speed_input.text())
            )

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(asdict(updated_settings), f, indent=4, ensure_ascii=False)

            print("Applied")
            self.settings_changed.emit(updated_settings)
            self.current_settings = updated_settings
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while saving: {str(e)}")