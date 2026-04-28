from config import *
import copy, random, time
from enum import Enum, auto
from game_logic.utils.vector2 import vec2
from game_logic.utils.snake import Snake
from game_logic.utils.tiles import *
from game_logic.utils.gamestate import *
from game_logic.utils.gamedata import *

from PyQt6.QtCore import QObject, pyqtSignal


class Game (QObject):
    game_state_changed = pyqtSignal(GameState)
    return_statistics = pyqtSignal(GameStatistics)

    def __init__(self):
        super().__init__()
        self._state = GameState.GAME_IS_PAUSED
        self._in_loop = False
        self.board = [[] for _ in range(WIDTH)] #board definition, seted in initialize()
        self.initialize()

    def initialize(self):
        """Creates a new game, clears board, points and all data"""

        self.statistics = GameStatistics()

        #self.board = [[Tile.NORMAL for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]  #fields on board are described by enum 'Tile'
        for i in range(WIDTH):
            self.board[i][:] = [Tile.NORMAL for _ in range(0, HEIGHT)]

        for x in range(0, WIDTH):
            self.board[x][0] = Tile.LIMIT
            self.board[x][HEIGHT - 1] = Tile.LIMIT
        for y in range(0, HEIGHT):
            self.board[0][y] = Tile.LIMIT
            self.board[WIDTH - 1][y] = Tile.LIMIT
    
        self.player = Snake(WIDTH//2, HEIGHT//2, HEIGHT)

        for segment in self.player.body:
            self.board[int(segment.x)][int(segment.y)] = Tile.SNAKE
        self.place_apple()

    def update_game(self, module):
        """
        Updates state of the game. Returns None if game is still running, otherwise \\
        list of collected data: [scored_points, turns, total_time]
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

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.LIMIT:
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
            
            self.place_apple()
        else:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE
            old_poz = self.player.body.pop()
            self.board[int(old_poz.x)][int(old_poz.y)] = Tile.NORMAL
        
        #self.game_state_changed.emit(GameState.GAME_IS_RUNNING)

    def place_apple(self):
            while True:
                self.apple = vec2(random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
                if self.board[int(self.apple.x)][int(self.apple.y)] == Tile.NORMAL:
                    self.board[int(self.apple.x)][int(self.apple.y)] = Tile.APPLE
                    break
    
    # def free(self):
    #     self.GAME_RUNNING = False
    #     while self.player.body:
    #         self.player.body.pop()
    def restart(self):
        #self.free()
        # while self.player.body:
        #     self.player.body.pop()
        self.initialize()
        self.game_state_changed.emit(GameState.GAME_SET_READY)
    
    def pause(self):
        #self.states.GAME_IS_RUNNING = False
        self._state = GameState.GAME_IS_PAUSED
        self.game_state_changed.emit(self._state)
    
    def resume(self):
        # if self.states.GAME_IS_OVER:
        #     return None
        # else:
        #     self.states.GAME_IS_RUNNING = True
        self._state = GameState.GAME_IS_RUNNING
        self.game_state_changed.emit(self._state)
    
    def run_in_loop(self):
        # if self.states.GAME_IS_OVER:
        #     return None
        # else:
        #     self.states.GAME_IS_RUNNING = True
        #     self.states.GAME_IN_LOOP = True
        if self._state == GameState.GAME_IS_PAUSED:
            self.resume()
        elif self._state == GameState.GAME_IS_OVER:
            self.restart()
            self._state = GameState.GAME_IS_RUNNING
        
        self._in_loop = True
        
    
    def end_game(self):
        stats = copy.copy(self.statistics)
        if self._in_loop:
            self.restart()
            self._state = GameState.GAME_IS_RUNNING
            self._in_loop = True
        else:
            self._state = GameState.GAME_IS_OVER
            self.game_state_changed.emit(self._state)
        
        self.return_statistics.emit(stats)
