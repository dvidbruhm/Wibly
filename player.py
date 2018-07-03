import pygame
from pygame.math import Vector2

from creature import Creature
import input_manager as InputManager
from body import Body

class Player(Creature):

    def __init__(self, position, rotation=90, scale=1, size=50, speed=200, turn_speed=5):
        Creature.__init__(self, position, rotation, scale, size, speed, turn_speed)

        self.head = Body(self, self.position, self.rotation, self.size, self.size, head=True)

        self.bodies = [
            self.head
        ]
        """
        for i in range(2):
            b = Body(self, self.position, self.rotation, self.size, self.size/2)
            b.attach_to(self.bodies[i])
            self.bodies.append(b)
        """
        for body in self.bodies:
            body.add_leg(self.size, 15, 20, (0, 0))
            body.add_leg(self.size, -15, 20, (0, 0))

    def update(self, dt):
        displacement = self.move_inputs()

        self.move_body(dt, displacement)

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