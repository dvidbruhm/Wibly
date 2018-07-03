from entity import Entity

entities = []

def add(entity):
    if isinstance(entity, Entity):
        entities.append(entity)
    else:
        raise Exception("Can only add Entity to list.")

def remove(entity):
    entities.remove(entity)