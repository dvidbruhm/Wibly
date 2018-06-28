import pygame

from entity import Entity
import input_manager as InputManager
from utils import *

import camera
import math

class Humanoid(Entity):
    def __init__(self, position, rotation=90, scale=1, size=1, speed=100):
        Entity.__init__(self, position, rotation, scale)
        self.size = size
        self.speed = speed

        self.rect = pygame.Rect((self.position[0] - self.size/2, self.position[1] - self.size/2, self.size, self.size/2))

        self.leg_length = size/2
        self.leg_dir = pygame.math.Vector2(0.5, 0.0).normalize()

        self.left_leg_pos = pygame.math.Vector2(self.rect.centerx - (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))
        self.left_leg_dest = pygame.math.Vector2(self.rect.centerx - (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))
        self.left_leg_start = pygame.math.Vector2(self.rect.centerx - (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))

        self.right_leg_pos = pygame.math.Vector2(self.rect.centerx + (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))
        self.right_leg_dest = pygame.math.Vector2(self.rect.centerx + (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))
        self.right_leg_start = pygame.math.Vector2(self.rect.centerx + (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))

        self.surface = pygame.Surface((self.rect.w, self.rect.h))


        self.time_to_move = 0.1
        self.left_timer = 0
        self.left_moving = False

        self.right_timer = 0
        self.right_moving = False

    def update(self, dt):
        self.move(dt)

    def render(self, screen):

        screen_pos = world_to_screen((self.rect.x, self.rect.y))
        screen_rect = world_to_screen(self.rect)



        surface = pygame.Surface((self.rect.w, self.rect.h))

        #body = pygame.draw.ellipse(screen, Color.WHITE, screen_rect, 2)
        body = pygame.draw.ellipse(surface, Color.WHITE, (0, 0, self.rect.w, self.rect.h), 2)

        old_center = screen_rect.center
        
        rotated_surface = pygame.transform.rotate(surface, self.rotation)
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = old_center

        rotated_surface.set_colorkey(Color.BLACK)
        screen.set_colorkey(Color.BLACK)

        screen.blit(rotated_surface, rotated_rect)



        left_leg = pygame.draw.line(screen, Color.WHITE, screen_rect.center, world_to_screen(self.left_leg_pos))
        left_foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.left_leg_pos), 5)

        right_leg = pygame.draw.line(screen, Color.WHITE, screen_rect.center, world_to_screen(self.right_leg_pos))
        left_foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.right_leg_pos), 5)

        #self.surface = pygame.transform.rotozoom(self.surface, self.rotation, self.scale)

        #screen.blit(self.surface, screen_pos)

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
            angle = angle_between(np.array(displacement), np.array((1, 0))) * 180 / 3.1416 + 90
            if displacement[1] >= 1:
                angle *= -1
            print(angle)
            self.rotation = angle 
            
            self.rect = self.rect.move(displacement.normalize() * self.speed * dt)

        self.move_legs(dt)

    def move_legs(self, dt):

        if self.left_leg_pos.distance_to(self.rect.center) > self.leg_length:
            self.left_leg_start = self.left_leg_pos
            self.left_leg_dest = pygame.math.Vector2(self.rect.centerx - (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))
            self.left_moving = True
            self.left_timer = 0


        if self.left_moving:
            self.left_timer += dt

            if self.left_timer >= self.time_to_move:
                self.left_moving = False
                self.left_timer = self.time_to_move

            self.left_leg_pos = self.left_leg_start.lerp(self.left_leg_dest, (self.left_timer / self.time_to_move))


        if self.right_leg_pos.distance_to(self.rect.center) > self.leg_length:
            self.right_leg_start = self.right_leg_pos
            self.right_leg_dest = pygame.math.Vector2(self.rect.centerx + (self.leg_dir.x * self.leg_length/2), self.rect.centery + (self.leg_dir.y * self.leg_length))
            self.right_moving = True
            self.right_timer = 0


        if self.right_moving:
            self.right_timer += dt

            if self.right_timer >= self.time_to_move:
                self.right_moving = False
                self.right_timer = self.time_to_move

            self.right_leg_pos = self.right_leg_start.lerp(self.right_leg_dest, (self.right_timer / self.time_to_move))


    def rel_to_world(self, rel_pos):
        world_pos = camera.main.position + rel_pos
        return world_pos

    def get_position(self):
        return pygame.math.Vector2(self.rect.center)