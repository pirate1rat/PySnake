class vec2:
    def __init__(self, x: int=None, y: int=None):
        self.x: int = x
        self.y: int = y
    
    def __add__(self, other):
        return vec2(self.x + other.x , self.y + other.y)
    
    def __sub__(self, other):
        return vec2(self.x - other.x , self.y - other.y)
    
    def __neg__(self):
        return vec2(-self.x , -self.y)


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __str__(self):
        return f"{self.x} , {self.y}"