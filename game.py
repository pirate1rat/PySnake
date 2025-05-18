import copy
import random
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

        self.board = [[1 for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]
        self.player = Snake(WIDTH//2, HEIGHT//2, HEIGHT)
        self.place_apple()

        for x in range(0, WIDTH):
            self.board[x][0] = 0
            self.board[x][HEIGHT - 1] = Tile.LIMIT.value
        for y in range(0, HEIGHT):
            self.board[0][y] = 0
            self.board[WIDTH - 1][y] = Tile.LIMIT.value
    
        for segment in self.player.body:
            self.board[int(segment.x)][int(segment.y)] = Tile.SNAKE.value

    def update_game(self, module) -> bool:
        if not self.GAME_RUNNING:
            return
        
        new_movec = module.Get_move(self.board, self.player)
        #print(new_movec)
        #move_tuple = moves.pop(0)
        #new_movec = vec2(move_tuple[0], move_tuple[1])

        if new_movec != vec2(0, 0) and self.player.movec != -new_movec:
            self.player.movec = copy.copy(new_movec)

        self.player.head += self.player.movec

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.LIMIT.value:
            self.GAME_OVER = True
            self.free()
            return
        elif self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.SNAKE.value:
            self.GAME_OVER = True
            self.free()
            return

        if self.board[int(self.player.head.x)][int(self.player.head.y)] == Tile.APPLE.value:
            self.player.body.insert(0, copy.copy(self.player.head))
            self.board[int(self.player.head.x)][int(self.player.head.y)] = Tile.SNAKE.value

            if len(self.player.body) == (WIDTH - 2)*(HEIGHT - 2):
                self.GAME_OVER = True
                self.free()
                return
            
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
            return
        self.GAME_RUNNING = True

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
            apple = vec2(random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
            if self.board[int(apple.x)][int(apple.y)] == Tile.NORMAL.value:
                self.board[int(apple.x)][int(apple.y)] = Tile.APPLE.value
                break
