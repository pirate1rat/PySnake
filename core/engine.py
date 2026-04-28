from PyQt6.QtCore import QObject, pyqtSignal

from utils.vector2 import vec2
from models.snake import Snake
from models.tiles import Tile
from models.game_state import GameState
from models.game_data import GameStatistics

from config import *

import copy
import random
import time


class Game (QObject):
    game_state_changed = pyqtSignal(GameState)
    return_statistics = pyqtSignal(GameStatistics)

    def __init__(self):
        super().__init__()
        self._run_in_loop = False
        self.board = [[] for _ in range(WIDTH)] # board definition, seted in initialize()
                                                # fields on board are described by enum 'Tile'
        self.initialize()

    def initialize(self, initial_state: GameState = GameState.GAME_IS_PAUSED):
        """
        Initialize a new game session by resetting the board and statistics.

        This method clears all existing game data, resets the board to its 
        starting configuration, and sets the engine's internal state to the 
        provided `initial_state` (by default GAME_IS_PAUSED). It is called during 
        the first launch or when restart is triggered.

        Args:
            initial_state: The state the game should enter upon initialization 
                (e.g. GameState.PAUSED or GameState.RUNNING).
        """

        self._state = initial_state
        self.statistics = GameStatistics()

        for i in range(WIDTH):
            self.board[i][:] = [Tile.EMPTY for _ in range(0, HEIGHT)]

        for x in range(0, WIDTH):
            self.board[x][0] = Tile.BORDER
            self.board[x][HEIGHT - 1] = Tile.BORDER
        for y in range(0, HEIGHT):
            self.board[0][y] = Tile.BORDER
            self.board[WIDTH - 1][y] = Tile.BORDER
    
        self.player = Snake(WIDTH//2, HEIGHT//2, HEIGHT)

        for segment in self.player.body:
            self.board[int(segment.x)][int(segment.y)] = Tile.SNAKE
        self.place_apple(self.board)

    def update_game(self, module):
        """
        Process a single game tick using the provided logic module.

        Executes the external algorithm within `module` to determine the next move.
        This method does not return values directly. Instead, it communicates 
        outcomes via signals:
        
        - Emits `game_state_changed` (GameState) when the game transitions 
        (e.g., to GameOver).
        - Emits `return_statistics` (GameStatistics) when the session ends 
        to provide final results.

        Args:
            module: An imported Python module containing the user's logic algorithm.
        """

        if self._state != GameState.GAME_IS_RUNNING:
            return 
        
        self.statistics.turns += 1

        timer_start = time.perf_counter()
        new_movec = module.Get_move(self.board, self.player, self.apple)
        timer_end = time.perf_counter()
        self.statistics.measured_time += timer_end - timer_start

        if new_movec != vec2(0, 0) and self.player.movec != -new_movec:
            self.player.movec = copy.copy(new_movec)

        self.player.head += self.player.movec

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.BORDER:
            self.end_game()
            return
        elif self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.SNAKE:
            self.end_game()
            return

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.APPLE:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE
            self.statistics.points += 1

            if len(self.player.body) == (WIDTH - 2)*(HEIGHT - 2):
                self.end_game()
                return
            
            self.place_apple(self.board)
        else:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE
            old_poz = self.player.body.pop()
            self.board[int(old_poz.x)][int(old_poz.y)] = Tile.EMPTY
        
    def place_apple(self, board):
        """
        Randomly position an apple on an empty tile of the game board.

        This method finds a random coordinate that is not currently occupied 
        by the snake and updates the `board` object in-place.

        Args:
            board: The game board matrix to be modified.
        """

        while True:
            self.apple = vec2(random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
            if board[int(self.apple.x)][int(self.apple.y)] == Tile.EMPTY:
                board[int(self.apple.x)][int(self.apple.y)] = Tile.APPLE
                break
    

    # --- Methods to comunicate with game ---
    def restart(self):
        self.initialize()
        self.game_state_changed.emit(GameState.GAME_SET_READY)
    
    def pause(self):
        self._state = GameState.GAME_IS_PAUSED
        self.game_state_changed.emit(self._state)
    
    def resume(self):
        self._state = GameState.GAME_IS_RUNNING
        self.game_state_changed.emit(self._state)
    
    def run_in_loop(self):
        if self._state == GameState.GAME_IS_PAUSED:
            self.resume()
        elif self._state == GameState.GAME_IS_OVER:
            self.restart()
            self._state = GameState.GAME_IS_RUNNING
        
        self._run_in_loop = True
        
    def end_game(self):
        """
        Finalize the current game session and broadcast final results.

        This method transitions the engine to the `GAME_IS_OVER` state and 
        captures a snapshot of the current session statistics. It ensures 
        that data is preserved before any potential engine reset.

        The following signals are emitted:
        - `game_state_changed` (GameState): Emitted with `GAME_IS_OVER` to 
        notify the UI and other components.
        - `return_statistics` (GameStatistics): Emitted with a copy of the 
        final statistics for visualization and logging.
        """

        stats = copy.copy(self.statistics)
        if self._run_in_loop:
            self.restart()
            self._state = GameState.GAME_IS_RUNNING
            self._run_in_loop = True
        else:
            self._state = GameState.GAME_IS_OVER
            self.game_state_changed.emit(self._state)
        
        self.return_statistics.emit(stats)
