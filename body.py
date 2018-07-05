import pygame
from pygame.math import Vector2

from color import Color
from utils import *
from entity import Entity
from leg import Leg
import physics

class Body(Entity):
    def __init__(self, creature, position, rotation, width, height, speed=30, head=False):
        Entity.__init__(self, position, rotation, 1, Vector2(1, 0))
        self.creature = creature
        self.height = height
        self.width = width
        self.head = head
        self.speed = speed

        self.legs = []
        self.direction = Vector2(1, 0)

        self.surface = pygame.Surface((self.width, self.height))

        self.attached_body = None

        self.physics_body = physics.add_circle_body(self.position, self.width/2, body_type="dynamic")

    def render(self, screen):
        super(Body, self).render(screen)

        screen_pos = world_to_screen(Vector2(self.physics_body.position))

        # Body surface
        body = pygame.draw.ellipse(self.surface, Color.WHITE, (0, 0, self.width, self.height), 1)

        # rotate body and correct center position
        old_center = screen_pos
        rotated_surface = pygame.transform.rotate(self.surface, self.rotation)
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = old_center

        # draw rotated body on screen
        rotated_surface.set_colorkey(Color.BLACK)
        screen.set_colorkey(Color.BLACK)
        screen.blit(rotated_surface, rotated_rect)

        # draw legs
        for leg in self.legs:
            leg.render(screen)

        if settings.debug:
            pygame.draw.circle(screen, Color.RED, world_to_screen(self.position), 3)
            pygame.draw.circle(screen, Color.GREEN, world_to_screen(self.lerp_pos), 3)
            if self.attached_body:
                pygame.draw.line(screen, Color.YELLOW, world_to_screen(self.get_position()), world_to_screen(self.attached_body.get_position()))

    def update(self, dt, new_pos, new_dir, moving):
        self.lerp_pos = new_pos
        self.direction = slerp(self.direction, new_dir, dt * self.creature.turn_speed)

        angle = angle_between(np.array(self.direction), np.array((0, -1)))

        if self.direction.x > 0:
            angle *= -1

        self.rotation = angle
        self.physics_body.angle = deg2rad(self.rotation)

        if not self.head:
            ### TODO: test some values for the velocity
            target_velocity = (new_pos - self.position) / 5
            self.physics_body.velocity = target_velocity#Vector2(self.physics_body.velocity).lerp(target_velocity, clamp(0, 1, dt * self.speed))
            self.position = Vector2(self.physics_body.position)
        else:
            if moving:
                target_velocity = new_dir * self.speed * dt
            else:
                target_velocity = Vector2(0, 0)

            self.physics_body.velocity = Vector2(self.physics_body.velocity).lerp(target_velocity, clamp(0, 1, dt * 10))
            self.position = Vector2(self.physics_body.position)

        for leg in self.legs:
            leg.update(dt)

    def add_leg(self, leg):
        self.legs.append(leg)

    def attach_to(self, other_body):
        self.attached_body = other_body
