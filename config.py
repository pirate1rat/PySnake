BLOCK_SIZE = 30 #in pixels
WIDTH = 12 #in blocks
HEIGHT = 12
GAME_SPEED = 1

registry = []

def register(solution_name):
    if solution_name not in registry:
        registry.append(solution_name)

def get_registry():
    return registry