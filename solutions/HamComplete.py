from config import *
register("HamComplete")

from utils.vector2 import vec2

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
                
    
    """for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            print(vec_field[j][i], " | ", end="")
        print()
    print()"""

def Get_move(board, snake):
    global first_time

    if first_time:
        first_time = False
        Compute()

    if vec_field[snake.head.x][snake.head.y] == -snake.movec:
        return vec2(1, 0)
    return vec_field[snake.head.x][snake.head.y]
    

    
