BLOCK_SIZE = 20 #in pixels
WIDTH = 20 #in blocks
HEIGHT = 20
GAME_SPEED = 1

registry = []

def register(solution_name):
    if solution_name not in registry:
        registry.append(solution_name)

def get_registry():
    return registry