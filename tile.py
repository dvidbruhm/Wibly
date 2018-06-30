import pygame

from entity import Entity
from utils import world_to_screen, Color

class Tile(Entity):
    def __init__(self, position, size=32):
        Entity.__init__(self, position, 0, pygame.math.Vector2(1, 1), pygame.math.Vector2(1, 0))
        self.size = size

    def render(self, screen):
        pos = world_to_screen(self.position)
        tile = pygame.draw.rect(screen, Color.WHITE, (pos[0], pos[1], self.size, self.size))
