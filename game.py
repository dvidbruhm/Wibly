import pygame
import sys

import input_manager as InputManager
import entity as EntityManager
import settings

from humanoid import Humanoid

pygame.init()
screen = pygame.display.set_mode(settings.window_size)
clock = pygame.time.Clock()

player = Humanoid(pygame.math.Vector2(200, 200), 20)
EntityManager.add(player)

def handle_inputs():
    InputManager.set_frame_pressed()
    InputManager.set_frame_events()

    for event in InputManager.events:
        if event.type == pygame.QUIT: 
            sys.exit()


def update():
    dt = clock.tick(30) / 1000 # in seconds

    for entity in EntityManager.entities:
        entity.update(dt)


def render():
    screen.fill((0, 0, 0))

    for entity in EntityManager.entities:
        entity.render(screen)

    pygame.display.flip()