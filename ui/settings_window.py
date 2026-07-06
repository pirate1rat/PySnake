from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SettingsWindow (QWidget):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Settings")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)