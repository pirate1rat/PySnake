from dataclasses import dataclass
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QColor, QPainter

from config import *

from models.tiles import Tile


@dataclass
class Colors:
    GREEN = (0, 255, 0)
    GREY = (69, 67, 61)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)


class BoardWidget (QWidget):
    def __init__(self, board, block_size):
        super().__init__()
        self._board = board
        self.WIDTH = len(board)
        self.HEIGHT = len(board[0])
        self.block_size = block_size
        self.setFixedSize(len(board) * block_size, len(board[0]) * block_size)
    
    def conv_to_rgb(self):
        rgb_board = [[Colors.BLACK for _ in range(0, self.HEIGHT)] for _ in range(0, self.WIDTH)]
        for i in range(0, self.HEIGHT):
            for j in range(0, self.WIDTH):
                match(self._board[j][i]):
                    case Tile.SNAKE: rgb_board[j][i] = Colors.GREEN
                    case Tile.LIMIT: rgb_board[j][i] = Colors.GREY
                    case Tile.APPLE: rgb_board[j][i] = Colors.RED
        return rgb_board

    def paintEvent(self, event):
        painter = QPainter(self)
        rgb_board = self.conv_to_rgb()

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                color = QColor(*rgb_board[x][y])
                painter.fillRect(
                    x*self.block_size,
                    y*self.block_size,
                    self.block_size,
                    self.block_size,
                    color
                )