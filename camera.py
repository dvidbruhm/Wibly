import pygame

from color import Color
import settings

class Camera():
    def __init__(self, size, lerp_speed=5, background_color=Color.BLACK):
        self.position = pygame.math.Vector2(0, 0)
        self.entity_to_follow = None
        self.lerp_speed = lerp_speed
        self.size = size
        self.background_color = background_color

    def is_visible(self, entity):
        pass

    def follow(self, entity):
        self.entity_to_follow = entity

    def render(self, screen):
        surface = pygame.Surface(self.size)
        rect = pygame.draw.rect(surface, self.background_color, (0, 0, self.size[0], self.size[1]))
        
        screen.blit(surface, pygame.math.Vector2(settings.window_size)/2 - self.size/2)
    
    def update(self, dt):
        if self.entity_to_follow is not None:
            self.position = self.position.lerp(self.entity_to_follow.get_position(), dt * self.lerp_speed)

    def is_visible(self, entity):
        difference = self.position - entity.get_position()

        if abs(difference[0]) < self.size[0]/2 and abs(difference[1]) < self.size[1]/2:
            return True
        else:
            return False
            
main = Camera(pygame.math.Vector2(settings.window_size))