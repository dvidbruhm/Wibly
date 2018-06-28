import pygame

import entity
import input_manager as InputManager
from utils import vec_to_pos, Color

class Humanoid(entity.Entity):
    def __init__(self, position, size, speed=50):
        entity.Entity.__init__(self, position)
        self.size = size
        self.speed = speed
        self.leg_length = size

        self.leg_dir = pygame.math.Vector2(0.5, 1).normalize()
        self.left_leg_pos = pygame.math.Vector2(self.position.x - (self.leg_dir.x * self.leg_length), self.position.y + (self.leg_dir.y * self.leg_length))
        self.right_leg_pos = pygame.math.Vector2(self.position.x + (self.leg_dir.x * self.leg_length), self.position.y + (self.leg_dir.y * self.leg_length))

    def update(self, dt):
        self.move(dt)

    def render(self, screen):
        print(Color.WHITE)
        body = pygame.draw.circle(screen, Color.WHITE, vec_to_pos(self.position), self.size, 2)

        left_leg = pygame.draw.line(screen, Color.WHITE, vec_to_pos(self.position), vec_to_pos(self.left_leg_pos))
        right_leg = pygame.draw.line(screen, Color.WHITE, vec_to_pos(self.position), vec_to_pos(self.right_leg_pos))

    def move(self, dt):
        up = InputManager.get_action(InputManager.Actions.MOVEUP)
        down = InputManager.get_action(InputManager.Actions.MOVEDOWN)
        left = InputManager.get_action(InputManager.Actions.MOVELEFT)
        right = InputManager.get_action(InputManager.Actions.MOVERIGHT)

        displacement = pygame.math.Vector2(0, 0)

        if up:
            displacement.y -= 1
        elif down:
            displacement.y += 1

        if right:
            displacement.x += 1
        elif left:
            displacement.x -= 1
            
        if displacement.length() > 0:
            self.position += displacement.normalize() * self.speed * dt

