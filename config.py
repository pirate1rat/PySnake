BLOCK_SIZE = 30 #in pixels
WIDTH = 8 #in blocks
HEIGHT = 8
GAME_SPEED = 200

registry = []

def register(solution_name):
    if solution_name not in registry:
        registry.append(solution_name)

def get_registry():
    return registry