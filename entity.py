entities = []

def add(entity):
    if isinstance(entity, Entity):
        entities.append(entity)
    else:
        raise Exception("Can only add Entity to list.")

def remove(entity):
    entities.remove(entity)



class Entity:
    def __init__(self, position, rotation, scale):
        self.position = position
        self.rotation = rotation
        self.scale = scale
    
    def update(self, dt):
        pass

    def render(self, screen):
        pass

    def get_position(self):
        pass