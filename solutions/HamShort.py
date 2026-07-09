from models.game_api import GameContext, Tile, Snake, vec2, register

@register
class HamShort():
    def __init__(self, ctx: GameContext):
        self.vec_field = [[None for _ in range(0, ctx.height)] for _ in range(0, ctx.width)]
        self.first_time = True

    def compute(self, ctx: GameContext):
        if ctx.width % 2 == 0:
            for c in range(1, ctx.width - 1):
                self.vec_field[c][ctx.height - 2] = vec2(-1, 0)
                if c % 2 != 0:
                    for y in range(0, ctx.height - 4):
                        self.vec_field[c][2+y] = vec2(0, -1)
                    self.vec_field[c][1] = vec2(1, 0)
                else:
                    for y in range(0, ctx.height - 4):
                        self.vec_field[c][1+y] = vec2(0, 1)
                    self.vec_field[c][ctx.height - 3] = vec2(1, 0)
            self.vec_field[1][ctx.height - 2] = vec2(0, -1)
            self.vec_field[ctx.width - 2][ctx.height - 3] = vec2(0, 1)
        elif ctx.height % 2 == 0:
            for r in range(1, ctx.height - 1):
                self.vec_field[1][r] = vec2(0, -1)
                if r % 2 != 0:
                    for x in range(0, ctx.width - 4):
                        self.vec_field[2+x][r] = vec2(1, 0)
                    self.vec_field[ctx.width - 2][r] = vec2(0, 1)
                else:
                    self.vec_field[2][r] = vec2(0, 1)
                    for x in range(0, ctx.width - 4):
                        self.vec_field[3+x][r] = vec2(-1, 0)
            self.vec_field[1][1] = vec2(1, 0)
            self.vec_field[2][ctx.height - 2] = vec2(-1, 0)
        else:
            for c in range(1, ctx.width - 3):
                self.vec_field[c][ctx.height - 2] = vec2(-1, 0)
                if c % 2 != 0:
                    for y in range(0, ctx.height - 4):
                        self.vec_field[c][2 + y] = vec2(0, -1)
                    self.vec_field[c][1] = vec2(1, 0)
                else:
                    for y in range(0, ctx.height - 4):
                        self.vec_field[c][1 + y] = vec2(0, 1)
                    self.vec_field[c][ctx.height - 3] = vec2(1, 0)

            for r in range(1, ctx.height - 2):
                if r % 2 != 0:
                    self.vec_field[ctx.width - 3][r] = vec2(1, 0)
                    self.vec_field[ctx.width - 2][r] = vec2(0, 1)
                else:
                    self.vec_field[ctx.width - 3][r] = vec2(0, 1)
                    self.vec_field[ctx.width - 2][r] = vec2(-1, 0)

            self.vec_field[ctx.width - 3][ctx.height - 2] = vec2(-1, 0)
            self.vec_field[ctx.width - 2][ctx.height - 2] = vec2(-1, 0)
            self.vec_field[1][ctx.height - 2] = vec2(0, -1)

    def get_move(self, ctx: GameContext) -> vec2:
        if self.first_time:
            self.first_time = False
            self.compute(ctx)

        if self.vec_field[ctx.snake.head.x][ctx.snake.head.y] == -ctx.snake.movec:
            return vec2(1, 0)

        if ctx.width % 2 == 0:
            if (1 < ctx.apple.x - ctx.snake.head.x and
                ctx.snake.head.y == 1 and
                ctx.board[ctx.snake.head.x + 1][ctx.snake.head.y] == Tile.EMPTY):
                return vec2(1, 0)
            elif (ctx.apple.x < ctx.snake.head.x and
                  ctx.snake.head.y == ctx.height - 3 and
                  ctx.board[ctx.snake.head.x][ctx.snake.head.y + 1] == Tile.EMPTY):
                return vec2(0, 1)
        elif ctx.height % 2 == 0:
            if (1 < ctx.apple.y - ctx.snake.head.y and
                ctx.snake.head.x == ctx.width - 2 and
                ctx.board[ctx.snake.head.x][ctx.snake.head.y + 1] == Tile.EMPTY):
                return vec2(0, 1)
            elif (ctx.apple.y < ctx.snake.head.y and
                  ctx.snake.head.x == 2 and
                  ctx.board[ctx.snake.head.x - 1][ctx.snake.head.y] == Tile.EMPTY):
                return vec2(-1, 0)
        else:
            if ctx.board[ctx.width - 2][ctx.height - 2] == Tile.APPLE:
                self.vec_field[ctx.width - 2][ctx.height - 3] = vec2(0, 1)
            else:
                self.vec_field[ctx.width - 2][ctx.height - 3] = vec2(-1, 0)

            if (1 < ctx.apple.x - ctx.snake.head.x and
                ctx.snake.head.y == 1 and
                ctx.snake.head.x < ctx.width - 3 and
                ctx.board[ctx.snake.head.x + 1][ctx.snake.head.y] == Tile.EMPTY):
                return vec2(1, 0)
            elif (ctx.apple.x < ctx.snake.head.x and
                  ctx.snake.head.y == ctx.height - 3 and
                  ctx.snake.head.x < ctx.width - 3 and
                  ctx.board[ctx.snake.head.x][ctx.snake.head.y + 1] == Tile.EMPTY):
                return vec2(0, 1)

        return self.vec_field[ctx.snake.head.x][ctx.snake.head.y]