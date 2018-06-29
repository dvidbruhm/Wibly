import pygame

from entity import Entity
import input_manager as InputManager
from utils import *

import camera
import math

class Leg():
    def __init__(self, attached_entity, lenght, angle, move_speed):
        self.lenght = lenght
        self.attached_entity = attached_entity
        
        self.direction = pygame.math.Vector2(angle, 0).normalize()

        self.position = pygame.math.Vector2(
            attached_entity.get_position().x + (self.direction.x * self.lenght), 
            attached_entity.get_position().y + (self.direction.y * self.lenght)
        )

        self.destination = pygame.math.Vector2(
            attached_entity.get_position().x + (self.direction.x * self.lenght), 
            attached_entity.get_position().y + (self.direction.y * self.lenght)
        )

        self.angle = angle
        self.move_speed = move_speed

    def render(self, screen):
        screen_pos = world_to_screen(self.attached_entity.get_position())
        leg = pygame.draw.line(screen, Color.WHITE, screen_pos, world_to_screen(self.position))
        foot = pygame.draw.circle(screen, Color.RED, world_to_screen(self.position), 5)
        dest = pygame.draw.circle(screen, Color.GREEN, world_to_screen(self.destination), 5)

    def update(self, dt, displacement):

        self.direction.x = displacement[0]
        self.direction.y = displacement[1]
        self.direction = self.direction.rotate(self.angle)

        self.move_foot()

        self.position = self.position.lerp(self.destination, dt * self.move_speed)

    def move_foot(self):

        body_pos = self.attached_entity.get_position()

        if self.position.distance_to(body_pos) > self.lenght:
            self.destination = pygame.math.Vector2(body_pos.x + (self.direction.x * self.lenght), body_pos.y + (self.direction.y * self.lenght))


class Humanoid(Entity):
    def __init__(self, position, rotation=90, scale=1, size=1, speed=200):
        Entity.__init__(self, position, rotation, scale)
        self.size = size
        self.speed = speed
        self.direction = pygame.math.Vector2(1, 0)

        self.turn_speed = 5

        self.rect = pygame.Rect((self.position[0] - self.size/2, self.position[1] - self.size/2, self.size, self.size/2))

        self.leg_lenght = size
        self.left_leg_dir = pygame.math.Vector2(-0.5, 0.0).normalize()
        self.right_leg_dir = pygame.math.Vector2(0.5, 0.0).normalize()

        self.left_leg_pos = pygame.math.Vector2(self.rect.centerx + (self.left_leg_dir.x * self.leg_lenght), self.rect.centery + (self.left_leg_dir.y * self.leg_lenght))
        self.left_leg_dest = pygame.math.Vector2(self.rect.centerx + (self.left_leg_dir.x * self.leg_lenght), self.rect.centery + (self.left_leg_dir.y * self.leg_lenght))

        self.right_leg_pos = pygame.math.Vector2(self.rect.centerx + (self.right_leg_dir.x * self.leg_lenght), self.rect.centery + (self.right_leg_dir.y * self.leg_lenght))
        self.right_leg_dest = pygame.math.Vector2(self.rect.centerx + (self.right_leg_dir.x * self.leg_lenght), self.rect.centery + (self.right_leg_dir.y * self.leg_lenght))

        self.surface = pygame.Surface((self.rect.w, self.rect.h))

        self.step_speed = 0.1
        self.current_delay_time = 0
        self.last_moved = "none"


        self.legs = [
            Leg(self, size, 25, 20),
            Leg(self, size, -25, 20),
            Leg(self, size*2, 45, 20),
            Leg(self, size*2, -45, 20)
        ]


    def update(self, dt):
        displacement = self.move_inputs()

        if displacement.length() > 0:
            displacement = displacement.normalize()
            self.move_body(dt, displacement)
            self.move_legs(dt, displacement)

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



        #left_leg = pygame.draw.line(screen, Color.WHITE, screen_rect.center, world_to_screen(self.left_leg_pos))
        #left_foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.left_leg_pos), 5)

        #right_leg = pygame.draw.line(screen, Color.WHITE, screen_rect.center, world_to_screen(self.right_leg_pos))
        #left_foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.right_leg_pos), 5)

        #self.surface = pygame.transform.rotozoom(self.surface, self.rotation, self.scale)

        #screen.blit(self.surface, screen_pos)

        for leg in self.legs:
            leg.render(screen)

        front = (screen_rect.centerx + self.direction.x*50, screen_rect.centery + self.direction.y*50)
        blu = pygame.draw.line(screen, Color.BLUE, screen_rect.center, front, 1)
    def move_inputs(self):

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

        return displacement

    def move_body(self, dt, displacement):

        self.direction = slerp(self.direction, pygame.math.Vector2(displacement), dt * 5)

        angle = angle_between(np.array(self.direction), np.array((0, -1)))

        if self.direction.x > 0:
            angle *= -1

        self.rotation = angle

        self.rect = self.rect.move(displacement * self.speed * dt)


    def move_legs(self, dt, displacement):

        


        for leg in self.legs:
            leg.update(dt, displacement)






        self.left_leg_dir.x = displacement[0]
        self.left_leg_dir.y = displacement[1]
        self.left_leg_dir = self.left_leg_dir.rotate(10)

        self.right_leg_dir.x = displacement[0]
        self.right_leg_dir.y = displacement[1]
        self.right_leg_dir = self.right_leg_dir.rotate(-10)


        self.current_delay_time += dt

        #if self.current_delay_time > self.step_speed:
        #    self.last_moved = "none"

        if self.left_leg_pos.distance_to(self.rect.center) > self.leg_lenght and self.current_delay_time >= self.step_speed and self.last_moved != "left":
            self.left_leg_dest = pygame.math.Vector2(self.rect.centerx + (self.left_leg_dir.x * self.leg_lenght), self.rect.centery + (self.left_leg_dir.y * self.leg_lenght))
            self.current_delay_time = 0
            self.last_moved = "left"

        self.left_leg_pos = self.left_leg_pos.lerp(self.left_leg_dest, dt * 20)


        if self.right_leg_pos.distance_to(self.rect.center) > self.leg_lenght and self.current_delay_time >= self.step_speed and self.last_moved != "right":
            self.right_leg_dest = pygame.math.Vector2(self.rect.centerx + (self.right_leg_dir.x * self.leg_lenght), self.rect.centery + (self.right_leg_dir.y * self.leg_lenght))
            self.current_delay_time = 0
            self.last_moved = "right"

        self.right_leg_pos = self.right_leg_pos.lerp(self.right_leg_dest, dt * 20)


    def rel_to_world(self, rel_pos):
        world_pos = camera.main.position + rel_pos
        return world_pos

    def get_position(self):
        return pygame.math.Vector2(self.rect.center)