import copy
import random
import time
from enum import Enum
from config import *
from utils.vector2 import vec2
from utils.snake import Snake
from utils.tiles import *
from dataclasses import dataclass


@dataclass
class Colors:
    GREEN = (0, 255, 0)
    GREY = (69, 67, 61)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

@dataclass
class GameState:
    """
    
    """

    GAME_IS_OVER: bool = False
    GAME_IS_RUNNING: bool = False
    GAME_IN_LOOP: bool = False
    
@dataclass
class GameStatistics:
    """
    
    """
    points: int = 0
    turns: int = 0
    measured_time: int = 0


class Game:
    def __init__(self):
        self.states = GameState()
        self.initialize()

    def initialize(self):
        """
        Creates a new game, clears board, points and all data
        """

        self.statistics = GameStatistics()

        self.board = [[Tile.NORMAL for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]  #fields on board are described by enum 'Tile'
        self.player = Snake(WIDTH//2, HEIGHT//2, HEIGHT)

        for x in range(0, WIDTH):
            self.board[x][0] = Tile.LIMIT
            self.board[x][HEIGHT - 1] = Tile.LIMIT
        for y in range(0, HEIGHT):
            self.board[0][y] = Tile.LIMIT
            self.board[WIDTH - 1][y] = Tile.LIMIT
    
        for segment in self.player.body:
            self.board[int(segment.x)][int(segment.y)] = Tile.SNAKE
        self.place_apple()

    def update_game(self, module):
        """
        Updates state of the game. Returns None if game is still running, otherwise \\
        list of collected data: [scored_points, turns, total_time]
        """

        self.statistics.turns += 1

        if not self.states.GAME_IS_RUNNING:
            return None
        
        timer_start = time.perf_counter()
        new_movec = module.Get_move(self.board, self.player, self.apple)
        timer_end = time.perf_counter()
        self.statistics.measured_time += timer_end - timer_start

        if new_movec != vec2(0, 0) and self.player.movec != -new_movec:
            self.player.movec = copy.copy(new_movec)

        self.player.head += self.player.movec

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.LIMIT:
            return self.end_game()
            
        elif self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.SNAKE:
            return self.end_game()

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.APPLE:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE
            self.statistics.points += 1

            if len(self.player.body) == (WIDTH - 2)*(HEIGHT - 2):
                return self.end_game() 
            
            self.place_apple()
        else:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE
            old_poz = self.player.body.pop()
            self.board[int(old_poz.x)][int(old_poz.y)] = Tile.NORMAL

    # def free(self):
    #     self.GAME_RUNNING = False
    #     while self.player.body:
    #         self.player.body.pop()
    def restart(self):
        #self.free()
        self.initialize()
    
    def pause(self):
        self.states.GAME_IS_RUNNING = False
    
    def resume(self):
        if self.states.GAME_IS_OVER:
            return None
        else:
            self.states.GAME_IS_RUNNING = True
    
    def in_loop(self):
        if self.states.GAME_IS_OVER:
            return None
        else:
            self.states.GAME_IS_RUNNING = True
            self.states.GAME_IN_LOOP = True
    
    def end_game(self):
        stats = copy(self.statistics)
        if self.states.GAME_IN_LOOP == True:
            self.restart()
            self.states.GAME_IS_RUNNING = True
            self.states.GAME_IN_LOOP = True
        else:
            self.states.GAME_IS_OVER = True
        return stats
        

    def conv_to_rgb(self):
        rgb_board = [[Colors.BLACK for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]
        for i in range(0, HEIGHT):
            for j in range(0, WIDTH):
                match(self.board[j][i]):
                    case Tile.SNAKE: rgb_board[j][i] = Colors.GREEN
                    case Tile.LIMIT: rgb_board[j][i] = Colors.GREY
                    case Tile.APPLE: rgb_board[j][i] = Colors.RED
        return rgb_board

    def place_apple(self):
        while True:
            self.apple = vec2(random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
            if self.board[int(self.apple.x)][int(self.apple.y)] == Tile.NORMAL:
                self.board[int(self.apple.x)][int(self.apple.y)] = Tile.APPLE
                break
