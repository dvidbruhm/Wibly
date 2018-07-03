import pygame
from pygame.math import Vector2

from color import Color
from utils import *
from entity import Entity

class Leg():
    def __init__(self, attached_body, length, angle, move_speed, offset=(0, 0), foot_size=5, walk=True):
        self.length = length
        self.attached_body = attached_body
        self.offset = offset
        self.foot_size = foot_size
        
        self.direction = Vector2(angle, 0).normalize()

        self.foot_position = Vector2(
            self.attached_body.get_position().x + (self.direction.x * self.length), 
            self.attached_body.get_position().y + (self.direction.y * self.length)
        )

        self.foot_destination = Vector2(
            self.attached_body.get_position().x + (self.direction.x * self.length), 
            self.attached_body.get_position().y + (self.direction.y * self.length)
        )

        self.angle = angle
        self.move_speed = move_speed

        self.punching = False
        self.walk = walk

    def render(self, screen):
        attach_pos = world_to_screen(self.attached_body.get_position() + Vector2(self.get_rel_offset()))

        leg = pygame.draw.line(screen, Color.WHITE, attach_pos, world_to_screen(self.foot_position))
        foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.foot_position), self.foot_size, 1)
        attach = pygame.draw.circle(screen, Color.WHITE, attach_pos, 2)

        if settings.debug:
            dest = pygame.draw.circle(screen, Color.GREEN, world_to_screen(self.foot_destination), self.foot_size)


    def update(self, dt):

        self.direction = self.attached_body.get_forward().rotate(self.angle)

        if self.punching and self.foot_position.distance_to(self.foot_destination) < 5:
            self.punching = False

        if not self.punching:
            self.move_foot()

        self.foot_position = self.foot_position.lerp(self.foot_destination, clamp(0, 1, dt * self.move_speed))

    def move_foot(self):

        attach_pos = self.attached_body.get_position() + self.get_rel_offset()

        if self.foot_position.distance_to(attach_pos) > self.length:
            self.foot_destination = Vector2(attach_pos.x + (self.direction.x * self.length), attach_pos.y + (self.direction.y * self.length))

        if not self.walk:
            self.foot_destination = Vector2(attach_pos.x + (self.direction.x * self.length), attach_pos.y + (self.direction.y * self.length))

    def get_rel_offset(self):
        forward = self.attached_body.get_forward()
        right = self.attached_body.get_right()
        return (right[0] * self.offset[0] + forward[0] * self.offset[1], right[1] * self.offset[0] + forward[1] * self.offset[1])

    def attach_to(self, body):
        self.attached_body = body

    def punch(self):
        self.punching = True
        self.foot_destination = self.attached_body.get_position() + self.attached_body.get_forward() * self.length * 10