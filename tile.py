import pygame

import physics
from entity import Entity
from color import Color
from utils import world_to_screen

class Tile(Entity):
    def __init__(self, position, size=32):
        Entity.__init__(self, position, 0, pygame.math.Vector2(1, 1), pygame.math.Vector2(1, 0))
        self.size = size

        corners = [
            (position[0] - self.size/2, position[1] - self.size/2),
            (position[0] - self.size/2, position[1] + self.size/2),
            (position[0] + self.size/2, position[1] + self.size/2),
            (position[0] + self.size/2, position[1] - self.size/2)
        ]

        self.physics_body = physics.add_polygon_body(corners)

    def render(self, screen):
        pos = world_to_screen(self.position)
        tile = pygame.draw.rect(screen, Color.WHITE, (pos[0] - self.size/2, pos[1] - self.size/2, self.size, self.size), 1)
