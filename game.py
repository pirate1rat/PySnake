import copy
import random
import time
from config import *
from utils.vector2 import vec2
from utils.snake import Snake
from utils.tiles import *

GREEN = (0, 255, 0)
GREY = (69, 67, 61)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.initz()

    def initz(self):
        self.GAME_OVER = False
        self.GAME_RUNNING = False
        self.GAME_LOOP = False

        self.points = 0
        self.turns = 0
        self.timer = 0

        self.board = [[1 for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]
        self.player = Snake(WIDTH//2, HEIGHT//2, HEIGHT)

        for x in range(0, WIDTH):
            self.board[x][0] = 0
            self.board[x][HEIGHT - 1] = Tile.LIMIT.value
        for y in range(0, HEIGHT):
            self.board[0][y] = 0
            self.board[WIDTH - 1][y] = Tile.LIMIT.value
    
        for segment in self.player.body:
            self.board[int(segment.x)][int(segment.y)] = Tile.SNAKE.value
        self.place_apple()

    def update_game(self, module) -> bool:
        self.turns += 1

        if not self.GAME_RUNNING:
            return None
        
        start = time.perf_counter()
        new_movec = module.Get_move(self.board, self.player, self.apple)
        end = time.perf_counter()
        self.timer += end - start

        if new_movec != vec2(0, 0) and self.player.movec != -new_movec:
            self.player.movec = copy.copy(new_movec)

        self.player.head += self.player.movec

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.LIMIT.value:
            return self.end_game()
            
        elif self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.SNAKE.value:
            return self.end_game()

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.APPLE.value:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE.value
            self.points += 1

            if len(self.player.body) == (WIDTH - 2)*(HEIGHT - 2):
                return self.end_game() 
            
            self.place_apple()
        else:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE.value
            old_poz = self.player.body.pop()
            self.board[int(old_poz.x)][int(old_poz.y)] = Tile.NORMAL.value

    def free(self):
        self.GAME_RUNNING = False
        while self.player.body:
            self.player.body.pop()
    def restart(self):
        self.free()
        self.initz()
    def pause(self):
        self.GAME_RUNNING = False
    def resume(self):
        if self.GAME_OVER:
            return None
        else:
            self.GAME_RUNNING = True
    def in_loop(self):
        if self.GAME_OVER:
            return None
        else:
            self.GAME_RUNNING = True
            self.GAME_LOOP = True
    def end_game(self):
        pt = self.points
        tr = self.turns
        tm = self.timer
        if self.GAME_LOOP == True:
            self.restart()
            self.GAME_RUNNING = True
            self.GAME_LOOP = True
        else:
            self.GAME_OVER = True
            self.free()
        test = [pt, tr, tm]
        return test

    def conv_to_rgb(self):
        rgb_board = [[BLACK for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]
        for i in range(0, HEIGHT):
            for j in range(0, WIDTH):
                match(self.board[j][i]):
                    case Tile.SNAKE.value: rgb_board[j][i] = GREEN
                    case Tile.LIMIT.value: rgb_board[j][i] = GREY
                    case Tile.APPLE.value: rgb_board[j][i] = RED
        return rgb_board

    def place_apple(self):
        while True:
            self.apple = vec2(random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
            if self.board[int(self.apple.x)][int(self.apple.y)] == Tile.NORMAL.value:
                self.board[int(self.apple.x)][int(self.apple.y)] = Tile.APPLE.value
                break
