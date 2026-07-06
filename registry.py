_registry = dict()

def register(cls):
    if cls not in _registry:
        _registry[cls.__name__] = cls
    return cls
    
def get_registry_str():
    return _registry.keys()

def get_registry():
    return _registry