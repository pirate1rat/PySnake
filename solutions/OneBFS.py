from models.game_api import GameContext, Tile, Snake, vec2, register

@register
class OneBFS():
    def __init__(self, ctx: GameContext):
        self.list_of_moves = list()

    def compute(self, ctx: GameContext) -> list: #BFS
        que = list()
        pat = list()
        moves = [[vec2(0, 0) for _ in range(ctx.height)] for _ in range(ctx.width)]

        pos = ctx.snake.head
        moves[int(ctx.snake.head.x)][int(ctx.snake.head.y)] = vec2(-1, -1)

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

            if ctx.board[int(pos.x)][int(pos.y)] == Tile.BORDER:
                continue
            if ctx.board[int(pos.x)][int(pos.y)] == Tile.SNAKE:
                continue

            if ctx.board[int(pos.x)][int(pos.y)] == Tile.APPLE:
                while pos != ctx.snake.head:
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
        
        if ctx.board[int(ctx.snake.head.x)][int(ctx.snake.head.y - 1)] == Tile.EMPTY:
            return [vec2(ctx.snake.head.x, ctx.snake.head.y - 1)]
        if ctx.board[int(ctx.snake.head.x - 1)][int(ctx.snake.head.y)] == Tile.EMPTY:
            return [vec2(ctx.snake.head.x - 1, ctx.snake.head.y)]
        if ctx.board[int(ctx.snake.head.x)][int(ctx.snake.head.y + 1)] == Tile.EMPTY:
            return [vec2(ctx.snake.head.x, ctx.snake.head.y + 1)]
        if ctx.board[int(ctx.snake.head.x + 1)][int(ctx.snake.head.y)] == Tile.EMPTY:
            return [vec2(ctx.snake.head.x + 1, ctx.snake.head.y)]
        
        return [vec2(ctx.snake.head.x + 1, ctx.snake.head.y)]

    def get_move(self, ctx: GameContext) -> vec2:
        if len(self.list_of_moves) == 0:
            path = self.compute(ctx) #BFS
            self.list_of_moves.append(path[0] - ctx.snake.head)
            for i in range(1, len(path) - 1):
                self.list_of_moves.append(path[i] - path[i - 1])
        
        return self.list_of_moves.pop(0)