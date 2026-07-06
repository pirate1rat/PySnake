registry = []

def register(solution_name):
    if solution_name not in registry:
        registry.append(solution_name)

def get_registry():
    return registry