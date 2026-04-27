from config import *
register("MultiBFS")

from game_logic.utils.snake import Snake
from game_logic.utils.vector2 import *
from game_logic.utils.tiles import *

def Compute(board: list, agent: Snake) -> list: #BFS
    que = list()
    pat = list()
    moves = [[vec2(0, 0) for _ in range(HEIGHT)] for _ in range(WIDTH)]

    pos = agent.head
    moves[int(agent.head.x)][int(agent.head.y)] = vec2(-1, -1)

    if moves[int(pos.x + 1)][int(pos.y)] == vec2(0, 0):
        que.append(vec2(pos.x + 1, pos.y))
        moves[int(pos.x + 1)][int(pos.y)] = vec2(pos.x, pos.y)
    if moves[int(pos.x - 1)][int(pos.y)] == vec2(0, 0):
        que.append(vec2(pos.x - 1, pos.y))
        moves[int(pos.x - 1)][int(pos.y)] = vec2(pos.x, pos.y)
    if moves[int(pos.x)][int(pos.y + 1)] == vec2(0, 0):
        que.append(vec2(pos.x, pos.y + 1))
        moves[int(pos.x)][int(pos.y + 1)] = vec2(pos.x, pos.y)
    if moves[int(pos.x)][int(pos.y - 1)] == vec2(0, 0):
        que.append(vec2(pos.x, pos.y - 1))
        moves[int(pos.x)][int(pos.y - 1)] = vec2(pos.x, pos.y)

    while len(que) != 0:
        pos = que.pop(0)
        #print(pos)

        if board[int(pos.x)][int(pos.y)] == Tile.LIMIT:
            continue
        if board[int(pos.x)][int(pos.y)] == Tile.SNAKE:
            continue

        if board[int(pos.x)][int(pos.y)] == Tile.APPLE:
            while pos != agent.head:
                pat.append(pos)
                #print("#######",pos)
                pos = moves[int(pos.x)][int(pos.y)]
            #print(pat)
            pat.reverse()
            return pat

        if moves[int(pos.x + 1)][int(pos.y)] == vec2(0, 0):
            que.append(vec2(pos.x + 1, pos.y))
            moves[int(pos.x + 1)][int(pos.y)] = vec2(pos.x, pos.y)
        if moves[int(pos.x - 1)][int(pos.y)] == vec2(0, 0):
            que.append(vec2(pos.x - 1, pos.y))
            moves[int(pos.x - 1)][int(pos.y)] = vec2(pos.x, pos.y)
        if moves[int(pos.x)][int(pos.y + 1)] == vec2(0, 0):
            que.append(vec2(pos.x, pos.y + 1))
            moves[int(pos.x)][int(pos.y + 1)] = vec2(pos.x, pos.y)
        if moves[int(pos.x)][int(pos.y - 1)] == vec2(0, 0):
            que.append(vec2(pos.x, pos.y - 1))
            moves[int(pos.x)][int(pos.y - 1)] = vec2(pos.x, pos.y)
    
    if board[int(agent.head.x)][int(agent.head.y - 1)] == Tile.NORMAL:
        return [vec2(agent.head.x, agent.head.y - 1)]
    if board[int(agent.head.x - 1)][int(agent.head.y)] == Tile.NORMAL:
        return [vec2(agent.head.x - 1, agent.head.y)]
    if board[int(agent.head.x)][int(agent.head.y + 1)] == Tile.NORMAL:
        return [vec2(agent.head.x, agent.head.y + 1)]
    if board[int(agent.head.x + 1)][int(agent.head.y)] == Tile.NORMAL:
        return [vec2(agent.head.x + 1, agent.head.y)]
    
    return [vec2(agent.head.x + 1, agent.head.y)]

list_of_moves = list()
def Get_move(board, snake, apple):
    global list_of_moves

    path = Compute(board, snake) #BFS
    return path[0] - snake.head