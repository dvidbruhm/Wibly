import pygame

import settings
from utils import world_to_screen, Color

entities = []

def add(entity):
    if isinstance(entity, Entity):
        entities.append(entity)
    else:
        raise Exception("Can only add Entity to list.")

def remove(entity):
    entities.remove(entity)



class Entity:
    def __init__(self, position, rotation, scale, direction):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.direction = direction
    
    def update(self, dt):
        pass

    def render(self, screen):
        if settings.debug:
            screen_pos = world_to_screen(self.position)
            # Draw forward and right vector
            forward = (screen_pos[0] + self.get_forward()[0]*50, screen_pos[1] + self.get_forward()[1]*50)
            right = (screen_pos[0] + self.get_right()[0]*50, screen_pos[1] + self.get_right()[1]*50)

            pygame.draw.line(screen, Color.BLUE, screen_pos, forward, 1)
            pygame.draw.line(screen, Color.GREEN, screen_pos, right, 1)

    def get_position(self):
        return self.position

    def get_rotation(self):
        return self.position

    def get_scale(self):
        return self.position

    def get_forward(self):
        return self.direction

    def get_right(self):
        return (-self.direction[1], self.direction[0])