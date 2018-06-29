import pygame

from pygame.math import Vector2

from entity import Entity
import input_manager as InputManager
from utils import *

import camera
import math

class Leg():
    def __init__(self, attached_entity, lenght, angle, move_speed, offset=(0, 0), foot_size=5):
        self.lenght = lenght
        self.attached_entity = attached_entity
        self.offset = offset
        self.foot_size = foot_size
        
        self.direction = Vector2(angle, 0).normalize()

        self.position = Vector2(
            attached_entity.get_position().x + (self.direction.x * self.lenght), 
            attached_entity.get_position().y + (self.direction.y * self.lenght)
        )

        self.destination = Vector2(
            attached_entity.get_position().x + (self.direction.x * self.lenght), 
            attached_entity.get_position().y + (self.direction.y * self.lenght)
        )

        self.angle = angle
        self.move_speed = move_speed

    def render(self, screen):
        screen_pos = world_to_screen(self.attached_entity.get_position())

        leg = pygame.draw.line(screen, Color.WHITE, tuple_add(screen_pos, self.get_rel_offset()), world_to_screen(self.position))
        foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.position), self.foot_size)
        #dest = pygame.draw.circle(screen, Color.GREEN, world_to_screen(self.destination), self.foot_size)

        attach_pos = self.attached_entity.get_position() + self.get_rel_offset()
        attach = pygame.draw.circle(screen, Color.WHITE, world_to_screen(attach_pos), 2)

    def update(self, dt, displacement):

        self.direction.x = displacement[0]
        self.direction.y = displacement[1]
        self.direction = self.direction.rotate(self.angle)

        self.move_foot()

        self.position = self.position.lerp(self.destination, dt * self.move_speed)

    def move_foot(self):

        attach_pos = self.attached_entity.get_position() + self.get_rel_offset()

        if self.position.distance_to(attach_pos) > self.lenght:
            self.destination = Vector2(attach_pos.x + (self.direction.x * self.lenght), attach_pos.y + (self.direction.y * self.lenght))

    def get_rel_offset(self):
        forward = self.attached_entity.get_forward()
        right = self.attached_entity.get_right()
        return (right[0] * self.offset[0] + forward[0] * self.offset[1], right[1] * self.offset[0] + forward[1] * self.offset[1])

class Creature(Entity):
    def __init__(self, position, rotation=90, scale=1, size=1, speed=200):
        Entity.__init__(self, position, rotation, scale)
        self.size = size
        self.speed = speed
        self.direction = Vector2(1, 0)

        self.turn_speed = 5

        self.rect = pygame.Rect((self.position[0] - self.size/2, self.position[1] - self.size/2, self.size, self.size/2))

        self.surface = pygame.Surface((self.rect.w, self.rect.h))

        self.step_speed = 0.1
        self.current_delay_time = 0
        self.last_moved = "none"


        self.legs = [
            Leg(self, size, 25, 15, offset=(10, 10)),
            Leg(self, size, -25, 20, offset=(-10, 10)),
            Leg(self, size, 45, 15, offset=(10, -10)),
            Leg(self, size, -45, 20, offset=(-10, -10))
        ]


    def update(self, dt):
        displacement = self.move_inputs()

        if displacement.length() > 0:
            displacement = displacement.normalize()
            self.move_body(dt, displacement)
            self.move_legs(dt, displacement)

    def render(self, screen):

        # screen positions
        screen_pos = world_to_screen((self.rect.x, self.rect.y))
        screen_rect = world_to_screen(self.rect)

        # Body surface
        surface = pygame.Surface((self.rect.w, self.rect.h))
        body = pygame.draw.ellipse(surface, Color.WHITE, (0, 0, self.rect.w, self.rect.h), 2)

        # rotate body and correct center position
        old_center = screen_rect.center
        rotated_surface = pygame.transform.rotate(surface, self.rotation)
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = old_center

        # draw rotated body on screen
        rotated_surface.set_colorkey(Color.BLACK)
        screen.set_colorkey(Color.BLACK)
        screen.blit(rotated_surface, rotated_rect)

        # draw legs
        for leg in self.legs:
            leg.render(screen)

        # Draw forward and right vector
        forward = (screen_rect.centerx + self.get_forward()[0]*50, screen_rect.centery + self.get_forward()[1]*50)
        right = (screen_rect.centerx + self.get_right()[0]*50, screen_rect.centery + self.get_right()[1]*50)

        #pygame.draw.line(screen, Color.BLUE, screen_rect.center, forward, 1)
        #pygame.draw.line(screen, Color.GREEN, screen_rect.center, right, 1)

    def move_inputs(self):

        up = InputManager.get_action(InputManager.Actions.MOVEUP)
        down = InputManager.get_action(InputManager.Actions.MOVEDOWN)
        left = InputManager.get_action(InputManager.Actions.MOVELEFT)
        right = InputManager.get_action(InputManager.Actions.MOVERIGHT)

        displacement = Vector2(0, 0)

        if up:
            displacement.y -= 1
        elif down:
            displacement.y += 1

        if right:
            displacement.x += 1
        elif left:
            displacement.x -= 1

        return displacement

    def move_body(self, dt, displacement):

        self.direction = slerp(self.direction, Vector2(displacement), dt * 5)

        angle = angle_between(np.array(self.direction), np.array((0, -1)))

        if self.direction.x > 0:
            angle *= -1

        self.rotation = angle

        self.rect = self.rect.move(displacement * self.speed * dt)


    def move_legs(self, dt, displacement):

        for leg in self.legs:
            leg.update(dt, displacement)


    def rel_to_world(self, rel_pos):
        world_pos = camera.main.position + rel_pos
        return world_pos

    def get_position(self):
        return Vector2(self.rect.center)

    def get_forward(self):
        return self.direction

    def get_right(self):
        return (-self.direction[1], self.direction[0])