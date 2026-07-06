from models.game_api import GameContext, Tile, Snake, vec2, register

@register
class HamComplete():
    def __init__(self, ctx: GameContext):
        self.vec_field = None
        self.first_time = True
        self.vec_field = [[None for _ in range(0, ctx.height)] for _ in range(0, ctx.width)]

    def compute(self, ctx: GameContext):
        if ctx.width % 2 == 0:
            for c in range(1, ctx.width - 1):
                self.vec_field[c][ctx.height - 2] = vec2(-1, 0)
                if c % 2 != 0:
                    for y in range(0, ctx.height - 4):
                        self.vec_field[c][2 + y] = vec2(0, -1)
                    self.vec_field[c][1] = vec2(1, 0)
                else:
                    for y in range(0, ctx.height - 4):
                        self.vec_field[c][1 + y] = vec2(0, 1)
                    self.vec_field[c][ctx.height - 3] = vec2(1, 0)
            self.vec_field[1][ctx.height - 2] = vec2(0, -1)
            self.vec_field[ctx.width - 2][ctx.height - 3] = vec2(0, 1)
        else:
            for r in range(1, ctx.height - 1):
                self.vec_field[1][r] = vec2(0, -1)
                if r % 2 != 0:
                    for x in range(0, ctx.width - 4):
                        self.vec_field[2 + x][r] = vec2(1, 0)
                    self.vec_field[ctx.width - 2][r] = vec2(0, 1)
                else:
                    self.vec_field[2][r] = vec2(0, 1)
                    for x in range(0, ctx.width - 4):
                        self.vec_field[3 + x][r] = vec2(-1, 0)
            self.vec_field[1][1] = vec2(1, 0)
            self.vec_field[2][ctx.height - 2] = vec2(-1, 0)

    def get_move(self, ctx: GameContext) -> vec2:
        if self.first_time:
            self.first_time = False
            self.compute(ctx)

        if self.vec_field[ctx.snake.head.x][ctx.snake.head.y] == -ctx.snake.movec:
            return vec2(1, 0)
        return self.vec_field[ctx.snake.head.x][ctx.snake.head.y]
