import pygame

from entity import Entity

class Camera(Entity):
    def __init__(self, size):
        Entity.__init__(self, pygame.math.Vector2(0, 0), 0, pygame.math.Vector2(1, 1))
        self.entity_to_follow = None

    def is_visible(self, entity):
        pass

    def follow(self, entity):
        self.entity_to_follow = entity
    
    def update(self, dt):
        if self.entity_to_follow is not None:
            self.position = self.entity_to_follow.get_position()

main = Camera((200, 200))