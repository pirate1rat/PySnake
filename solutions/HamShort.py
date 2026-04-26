from config import *
register("HamShort")

from game_logic.utils.vector2 import vec2
from game_logic.utils.tiles import *

vec_field = [[None for _ in range(0, HEIGHT)] for _ in range(0, WIDTH)]
first_time = True

def Compute():
    global vec_field

    if WIDTH % 2 == 0:
        for c in range(1, WIDTH - 1):
            vec_field[c][HEIGHT - 2] = vec2(-1, 0)
            if c % 2 != 0:
                for y in range(0, HEIGHT - 4):
                    vec_field[c][2+y] = vec2(0, -1)
                vec_field[c][1] = vec2(1, 0)
            else:
                for y in range(0, HEIGHT - 4):
                    vec_field[c][1+y] = vec2(0, 1)
                vec_field[c][HEIGHT - 3] = vec2(1, 0)
        vec_field[1][HEIGHT - 2] = vec2(0, -1)
        vec_field[WIDTH - 2][HEIGHT - 3] = vec2(0, 1)
    else:
        for r in range(1, HEIGHT - 1):
            vec_field[1][r] = vec2(0, -1)
            if r % 2 != 0:
                for x in range(0, WIDTH - 4):
                    vec_field[2+x][r] = vec2(1, 0)
                vec_field[WIDTH - 2][r] = vec2(0, 1)
            else:
                vec_field[2][r] = vec2(0, 1)
                for x in range(0, WIDTH - 4):
                    vec_field[3+x][r] = vec2(-1, 0)
        vec_field[1][1] = vec2(1, 0)
        vec_field[2][HEIGHT - 2] = vec2(-1, 0)

def Get_move(board, snake, apple):
    global first_time

    if first_time:
        first_time = False
        Compute()

    if vec_field[snake.head.x][snake.head.y] == -snake.movec:
        return vec2(1, 0)
    

    if WIDTH % 2 == 0:
        if (1 < apple.x - snake.head.x and snake.head.y == 1 and
            board[snake.head.x + 1][snake.head.y] == Tile.NORMAL):
            return vec2(1, 0)
        elif (apple.x < snake.head.x and snake.head.y == HEIGHT - 3 and 
            board[snake.head.x][snake.head.y + 1] == Tile.NORMAL):
            return vec2(0, 1)
    elif HEIGHT % 2 == 0:
        pass

    return vec_field[snake.head.x][snake.head.y]
    

    
