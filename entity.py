entities = []

def add(entity):
    if isinstance(entity, Entity):
        entities.append(entity)
    else:
        raise Exception("Can only add Entity to list.")

def remove(entity):
    entities.remove(entity)



class Entity:
    def __init__(self, position):
        self.position = position
    
    def update(self, dt):
        pass

    def render(self, screen):
        pass