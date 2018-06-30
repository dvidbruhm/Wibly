import pygame
from pygame.math import Vector2
import math

from entity import Entity
import input_manager as InputManager
from utils import *
from body import Body

import camera
import math

class Creature(Entity):
    def __init__(self, position, rotation=90, scale=1, size=1, speed=200, turn_speed=5):
        Entity.__init__(self, position, rotation, scale, Vector2(1, 0))
        self.size = size
        self.speed = speed

        self.turn_speed = turn_speed

        self.head = Body(self, self.position, self.rotation, self.size, self.size, head=True)

        self.bodies = [
            self.head
        ]
        for i in range(10):
            self.bodies.append(Body(self, self.position, self.rotation, int(self.size * ((math.sin(i)+1.5)/2)), self.size/2))

        for body in self.bodies:
            body.add_leg(self.size, 15, 20, (body.width/2, 0))
            body.add_leg(self.size, -15, 20, (-body.width/2, 0))

        self.last_displacement = Vector2(1, 0)


    def update(self, dt):
        displacement = self.move_inputs()

        if displacement.length() > 0:
            self.last_displacement = displacement

        self.move_body(dt, displacement)

    def render(self, screen):

        for body in self.bodies:
            body.render(screen)


        # draw legs
        #for leg in self.legs:
        #    leg.render(screen)
    
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

        if displacement.length() > 0:
            displacement = displacement.normalize()
            self.direction = slerp(self.direction, Vector2(displacement), dt * 5)
            self.position = self.position + displacement * self.speed * dt
            angle = angle_between(np.array(self.direction), np.array((0, -1)))

            if self.direction.x > 0:
                angle *= -1

            self.rotation = angle

        for i in range(len(self.bodies)):
            body = self.bodies[i]
            if i != 0:
                prev_body = self.bodies[i-1]
                pos = prev_body.rect.center - prev_body.direction*(body.height + prev_body.height)/2
                if displacement.length() > 0:
                    dir = prev_body.direction
                else:
                    dir = body.direction
                body.update(dt, pos, dir)
            else:
                pos = self.get_position()
                body.update(dt, pos, self.direction)

    def rel_to_world(self, rel_pos):
        world_pos = camera.main.position + rel_pos
        return world_pos

