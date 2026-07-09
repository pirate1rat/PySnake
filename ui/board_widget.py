from dataclasses import dataclass
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QColor, QPainter

from registry import *

from models.tiles import Tile

limiting_size = 16
default_block_size = 28

@dataclass
class Colors:
    GREEN = (0, 120, 72)
    GREY = (69, 67, 61)
    RED = (255, 0, 0)
    LIGHT_GREY = (192, 192, 192)


class BoardWidget (QWidget):
    def __init__(self, board):
        super().__init__()
        self.setFixedSize(450, 450)
        self.initialize(board)

    def initialize(self, board):
        self._board = board
        self.WIDTH = len(board)
        self.HEIGHT = len(board[0])

        if limiting_size < self.WIDTH or limiting_size < self.HEIGHT:
            self.block_size = int(448 / (max(self.WIDTH, self.HEIGHT)))
        else:
            self.block_size = default_block_size

    def paintEvent(self, event):
        painter = QPainter(self)
        
        actual_board_width = self.WIDTH * self.block_size
        actual_board_height = self.HEIGHT * self.block_size

        offset_x = (self.width() - actual_board_width) // 2
        offset_y = (self.height() - actual_board_height) // 2

        painter.translate(offset_x, offset_y)

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                tile = self._board[x][y]
                
                match tile:
                    case Tile.SNAKE: 
                        color = QColor(*Colors.GREEN)
                    case Tile.APPLE: 
                        color = QColor(*Colors.RED)
                    case Tile.BORDER: 
                        color = QColor(*Colors.GREY)
                    case _: 
                        color = QColor(*Colors.LIGHT_GREY)

                painter.fillRect(
                    x * self.block_size, 
                    y * self.block_size, 
                    self.block_size - 1,
                    self.block_size - 1, 
                    color
                )