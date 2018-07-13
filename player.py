import pygame
from pygame.math import Vector2

from creature import Creature
import input_manager as InputManager
from body import Body
from leg import Leg

class Player(Creature):

    def __init__(self, position, rotation=90, scale=1, size=50, speed=200, turn_speed=5):
        Creature.__init__(self, position, rotation, scale, size, speed, turn_speed)

        self.head = Body(self, self.position, self.rotation, self.size, self.size, head=True, speed=speed)

        self.bodies.append(self.head)

        for i in range(5):
            b = Body(self, self.position, self.rotation, self.size/2, self.size/2, speed=10)
            b.attach_to(self.bodies[i])
            self.bodies.append(b)
        
        #arm1 = Leg(self.head, 10, 90, 30, offset=(self.head.width/2, 0), foot_size=10, walk=False)
        #self.head.add_leg(arm1)
        #arm2 = Leg(self.head, 10, -90, 30, offset=(-self.head.width/2, 0), foot_size=10, walk=False)
        #self.head.add_leg(arm2)
        #self.arms.append(arm1)
        #self.arms.append(arm2)

        for body in self.bodies:
            body.add_leg(Leg(body, self.size, 15, 20, offset=(body.width/2 + 5, 0), foot_size=5))
            body.add_leg(Leg(body, self.size, -15, 20, offset=(-body.width/2 - 5, 0), foot_size=5))

        self.arm_counter = 0

    def update(self, dt):
        displacement = self.move_inputs()

        if len(self.arms) > 0:
            punch = self.offense_inputs()

            if punch:
                self.arms[self.arm_counter].punch()
                self.arm_counter = (self.arm_counter + 1) % len(self.arms)
        
        self.move_bodies(dt, displacement)
        
    def offense_inputs(self):

        punch = InputManager.get_action_down(InputManager.Actions.PUNCH)

        return punch

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