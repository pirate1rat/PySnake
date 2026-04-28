from utils.vector2 import vec2

class Snake:
    def __init__(self, x: int, y: int, HEIGHT: int, length: int = 3) -> None:
        self.body = list()
        self.head = vec2(x, y)
        self.movec = vec2(0, -1)
        self.body.append(vec2(self.head.x, self.head.y))

        if length > ((HEIGHT - 2) // 2):
            length = ((HEIGHT - 2) // 2) - 1
        for i in range(1, length):
            self.body.append(vec2(x, y + i))
