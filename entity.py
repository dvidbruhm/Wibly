import pygame

import settings
from color import Color
from utils import world_to_screen

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
            forward = (screen_pos[0] + self.get_forward()[0]*20, screen_pos[1] + self.get_forward()[1]*20)
            right = (screen_pos[0] + self.get_right()[0]*20, screen_pos[1] + self.get_right()[1]*20)

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
        return pygame.math.Vector2(-self.direction[1], self.direction[0])