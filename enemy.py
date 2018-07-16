from pygame.math import Vector2
import random

from creature import Creature
from body import Body
from leg import Leg
from physics import Categories

class Enemy(Creature):
    def __init__(self, position, rotation=90, scale=1, size=50, speed=100, turn_speed=5):
        Creature.__init__(self, position, rotation, scale, size, speed, turn_speed)

        self.head = Body(self, self.position, self.rotation, self.size*2, self.size*2, Categories.ENEMY, head=True, speed=speed)

        self.bodies.append(self.head)

        for i in range(4):
            b = Body(self, self.position, self.rotation, self.size, self.size, Categories.ENEMY, speed=30)
            b.attach_to(self.bodies[i])
            self.bodies.append(b)

        for body in self.bodies:    
            leg = Leg(body, self.size*2, 15, 40, (body.width/2, 0), 3)
            body.add_leg(leg)
            leg = Leg(body, self.size*2, -15, 40, (-body.width/2, 0), 3)
            body.add_leg(leg)

        self.wander_time = 2
        self.timer = random.random() * self.wander_time

        self.displacement = Vector2(0, 0)

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.wander_time:
            self.timer = 0
            if random.random() > 0.5:
                self.displacement = Vector2(random.random()-0.5, random.random()-0.5).normalize()
            else:
                self.displacement = Vector2(0, 0)

        self.move_bodies(dt, self.displacement)
