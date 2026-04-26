from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QGuiApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySnake")
        self.resize(1050, 950)
        self.center()
        #self.setWindowIcon(QIcon(""))

    def center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())