import pygame
from pygame.math import Vector2

import physics
from color import Color
from utils import *

class Map:
    def __init__(self, size):
        self.size = size

        top_left = Vector2(-self.size/2, -self.size/2)
        top_right = Vector2(self.size/2, -self.size/2)
        bottom_right = Vector2(self.size/2, self.size/2)
        bottom_left = Vector2(-self.size/2, self.size/2)

        self.corners = [top_left, top_right, bottom_right, bottom_left]

        self.make_borders()
    
    def make_borders(self):

        physics.add_segment_body(self.corners[0], self.corners[1], category=physics.Categories.WALL)
        physics.add_segment_body(self.corners[1], self.corners[2], category=physics.Categories.WALL)
        physics.add_segment_body(self.corners[2], self.corners[3], category=physics.Categories.WALL)
        physics.add_segment_body(self.corners[3], self.corners[0], category=physics.Categories.WALL)
    
    def render_borders(self, screen):
        pygame.draw.line(screen, Color.WHITE, world_to_screen(self.corners[0]), world_to_screen(self.corners[1]))
        pygame.draw.line(screen, Color.WHITE, world_to_screen(self.corners[1]), world_to_screen(self.corners[2]))
        pygame.draw.line(screen, Color.WHITE, world_to_screen(self.corners[2]), world_to_screen(self.corners[3]))
        pygame.draw.line(screen, Color.WHITE, world_to_screen(self.corners[3]), world_to_screen(self.corners[0]))

    def render(self, screen):
        self.render_borders(screen)