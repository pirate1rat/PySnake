from config import *
register("OneBFS")

from utils.snake import Snake
from utils.vector2 import *
from utils.tiles import *

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

        if board[int(pos.x)][int(pos.y)] == Tile.LIMIT.value:
            continue
        if board[int(pos.x)][int(pos.y)] == Tile.SNAKE.value:
            continue

        if board[int(pos.x)][int(pos.y)] == Tile.APPLE.value:
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
    
    if board[int(agent.head.x)][int(agent.head.y - 1)] == Tile.NORMAL.value:
        return [vec2(agent.head.x, agent.head.y - 1)]
    if board[int(agent.head.x - 1)][int(agent.head.y)] == Tile.NORMAL.value:
        return [vec2(agent.head.x - 1, agent.head.y)]
    if board[int(agent.head.x)][int(agent.head.y + 1)] == Tile.NORMAL.value:
        return [vec2(agent.head.x, agent.head.y + 1)]
    if board[int(agent.head.x + 1)][int(agent.head.y)] == Tile.NORMAL.value:
        return [vec2(agent.head.x + 1, agent.head.y)]
    
    return [vec2(agent.head.x + 1, agent.head.y)]

list_of_moves = list()
def Get_move(board, snake):
    global list_of_moves

    if len(list_of_moves) == 0:
        path = Compute(board, snake) #BFS
        list_of_moves.append(path[0] - snake.head)
        for i in range(1, len(path) - 1):
            list_of_moves.append(path[i] - path[i - 1])
    
    return list_of_moves.pop(0)