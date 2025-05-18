import snake as sk
import pygame
import sys
import time
import copy
import random
from enum import Enum

BLOCK_SIZE = int(20) #in px
WIDTH = 20 #in blocks
HIGHT = 20
GAME_SPEED = 100
count = 0

GREEN = (0, 255, 0)
GREY = (69, 67, 61)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

res = (WIDTH*BLOCK_SIZE, HIGHT*BLOCK_SIZE)
screen = pygame.display.set_mode(res)
board = [[1 for _ in range(0, WIDTH)] for _ in range(0, HIGHT)]
agent = sk.Snake(WIDTH//2, HIGHT//2, HIGHT)
agent_path = list()
apple = pygame.Vector2(random.randint(1, WIDTH - 2), random.randint(1, HIGHT - 2))

class Tile(Enum):
    LIMIT = 0
    NORMAL = 1
    SNAKE = 2
    APPLE = 3

def BFS() -> list:
    que = list()
    pat = list()
    moves = [[pygame.Vector2(0, 0) for _ in range(WIDTH)] for _ in range(HIGHT)]

    pos = agent.head
    moves[int(agent.head.x)][int(agent.head.y)] = pygame.Vector2(-1, -1)

    if moves[int(pos.x + 1)][int(pos.y)] == pygame.Vector2(0, 0):
        que.append(pygame.Vector2(pos.x + 1, pos.y))
        moves[int(pos.x + 1)][int(pos.y)] = pygame.Vector2(pos.x, pos.y)
    if moves[int(pos.x - 1)][int(pos.y)] == pygame.Vector2(0, 0):
        que.append(pygame.Vector2(pos.x - 1, pos.y))
        moves[int(pos.x - 1)][int(pos.y)] = pygame.Vector2(pos.x, pos.y)
    if moves[int(pos.x)][int(pos.y + 1)] == pygame.Vector2(0, 0):
        que.append(pygame.Vector2(pos.x, pos.y + 1))
        moves[int(pos.x)][int(pos.y + 1)] = pygame.Vector2(pos.x, pos.y)
    if moves[int(pos.x)][int(pos.y - 1)] == pygame.Vector2(0, 0):
        que.append(pygame.Vector2(pos.x, pos.y - 1))
        moves[int(pos.x)][int(pos.y - 1)] = pygame.Vector2(pos.x, pos.y)

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

        if moves[int(pos.x + 1)][int(pos.y)] == pygame.Vector2(0, 0):
            que.append(pygame.Vector2(pos.x + 1, pos.y))
            moves[int(pos.x + 1)][int(pos.y)] = pygame.Vector2(pos.x, pos.y)
        if moves[int(pos.x - 1)][int(pos.y)] == pygame.Vector2(0, 0):
            que.append(pygame.Vector2(pos.x - 1, pos.y))
            moves[int(pos.x - 1)][int(pos.y)] = pygame.Vector2(pos.x, pos.y)
        if moves[int(pos.x)][int(pos.y + 1)] == pygame.Vector2(0, 0):
            que.append(pygame.Vector2(pos.x, pos.y + 1))
            moves[int(pos.x)][int(pos.y + 1)] = pygame.Vector2(pos.x, pos.y)
        if moves[int(pos.x)][int(pos.y - 1)] == pygame.Vector2(0, 0):
            que.append(pygame.Vector2(pos.x, pos.y - 1))
            moves[int(pos.x)][int(pos.y - 1)] = pygame.Vector2(pos.x, pos.y)
    
    if board[int(agent.head.x)][int(agent.head.y - 1)] == Tile.NORMAL.value:
        return [pygame.Vector2(agent.head.x, agent.head.y - 1)]
    if board[int(agent.head.x - 1)][int(agent.head.y)] == Tile.NORMAL.value:
        return [pygame.Vector2(agent.head.x - 1, agent.head.y)]
    if board[int(agent.head.x)][int(agent.head.y + 1)] == Tile.NORMAL.value:
        return [pygame.Vector2(agent.head.x, agent.head.y + 1)]
    if board[int(agent.head.x + 1)][int(agent.head.y)] == Tile.NORMAL.value:
        return [pygame.Vector2(agent.head.x + 1, agent.head.y)]
    
    return [pygame.Vector2(agent.head.x + 1, agent.head.y)]


def Initz()->None:
    global agent_path

    for x in range(0, WIDTH):
        board[x][0] = 0
        board[x][HIGHT - 1] = 0
    for y in range(0, HIGHT):
        board[0][y] = 0
        board[WIDTH - 1][y] = 0
    
    for segment in agent.body:
        board[int(segment.x)][int(segment.y)] = Tile.SNAKE.value
    
    board[int(apple.x)][int(apple.y)] = Tile.APPLE.value

def UpdateGame() -> bool:
    global count, agent_path
    count += 1
    
    #time.sleep(2)
    #keyboard input
    #keys = pygame.key.get_pressed()
    #new_movec = pygame.Vector2(0, 0)
    #if keys[pygame.K_s]:
    #    new_movec = pygame.Vector2(0, 1)
    #if keys[pygame.K_w]:
    #    new_movec = pygame.Vector2(0, -1)
    #if keys[pygame.K_d]:
    #    new_movec = pygame.Vector2(1, 0)
    #if keys[pygame.K_a]:
    #    new_movec = pygame.Vector2(-1, 0)

    if count == GAME_SPEED:
        count = 0

        if len(agent_path) == 0:
            agent_path = BFS()
            print(agent_path)
        new_movec = agent_path.pop(0) - agent.head
        print(new_movec, agent.head)
        agent.movec = copy.copy(new_movec)

        agent.head += agent.movec

        if board[int(agent.head.x)][int(agent.head.y)] == Tile.LIMIT.value:
            print(len(agent.body))
            return False
        elif board[int(agent.head.x)][int(agent.head.y)] == Tile.SNAKE.value:
            print(len(agent.body))
            return False

        if board[int(agent.head.x)][int(agent.head.y)] == Tile.APPLE.value:
            agent.body.insert(0, copy.copy(agent.head))
            board[int(agent.head.x)][int(agent.head.y)] = Tile.SNAKE.value
            while True:
                apple = pygame.Vector2(random.randint(1, WIDTH - 2), random.randint(1, HIGHT - 2))
                if board[int(apple.x)][int(apple.y)] == Tile.NORMAL.value:
                    board[int(apple.x)][int(apple.y)] = Tile.APPLE.value
                    break
        else:
            agent.body.insert(0, copy.copy(agent.head))
            board[int(agent.head.x)][int(agent.head.y)] = Tile.SNAKE.value
            old_poz = agent.body.pop()
            board[int(old_poz.x)][int(old_poz.y)] = Tile.NORMAL.value
    

    return True

def ComposeFrame() -> None:
    #drawing
    screen.fill(BLACK)
    for x in range(0, WIDTH):
        for y in range(0, HIGHT):
            match board[x][y]:
                case Tile.LIMIT.value:
                    pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                case Tile.APPLE.value:
                    pygame.draw.rect(screen, RED, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                case Tile.SNAKE.value:
                    pygame.draw.rect(screen, GREEN, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                case _:
                    pass
    pygame.display.flip()

#main
Initz()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    if not UpdateGame():
        break
    ComposeFrame()
    