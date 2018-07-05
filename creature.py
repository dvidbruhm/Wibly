import pygame
from pygame.math import Vector2
import math

from entity import Entity
import input_manager as InputManager
from utils import *
from body import Body
from color import Color

import camera

class Creature(Entity):
    def __init__(self, position, rotation=90, scale=1, size=50, speed=300, turn_speed=5):
        Entity.__init__(self, position, rotation, scale, Vector2(1, 0))
        self.size = size
        self.speed = speed

        self.turn_speed = turn_speed

        self.head = None
        self.bodies = []
        self.arms = []

    def render(self, screen):
        for body in self.bodies:
            body.render(screen)
        
        if settings.debug:
            pygame.draw.circle(screen, Color.RED, world_to_screen(self.position), 3)

    def move_bodies(self, dt, displacement):

        self.position = Vector2(self.head.physics_body.position)
        moving = False
        if displacement.length() > 0:
            moving = True
            displacement = displacement.normalize()
            self.direction = slerp(self.direction, Vector2(displacement), dt * self.turn_speed)
            angle = angle_between(np.array(self.direction), np.array((0, -1)))

            if self.direction.x > 0:
                angle *= -1

            self.rotation = angle

        for i in range(len(self.bodies)):
            body = self.bodies[i]
            if i != 0:
                prev_body = self.bodies[i-1]
                pos = prev_body.position - prev_body.get_forward()*(body.height + prev_body.height + 5) / 2
                #if displacement.length() > 0:
                #    dir = prev_body.direction
                #else:
                #    dir = body.direction
                dir = prev_body.direction
                body.update(dt, pos, dir, moving)
            else:
                pos = self.get_position()
                body.update(dt, pos, self.direction, moving)


