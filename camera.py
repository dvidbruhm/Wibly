import pygame

class Camera():
    def __init__(self, size, lerp_speed=5):
        self.position = pygame.math.Vector2(0, 0)
        self.entity_to_follow = None
        self.lerp_speed = lerp_speed

    def is_visible(self, entity):
        pass

    def follow(self, entity):
        self.entity_to_follow = entity
    
    def update(self, dt):
        if self.entity_to_follow is not None:
            self.position = self.position.lerp(self.entity_to_follow.get_position(), dt * self.lerp_speed)

main = Camera((200, 200))