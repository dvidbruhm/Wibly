import pygame
import sys
import pymunk
import pymunk.pygame_util

import input_manager as InputManager
import entity_manager as EntityManager
import settings
import camera
import physics

from player import Player
from enemy import Enemy
from tile import Tile

## Init pygame
pygame.init()
screen = pygame.display.set_mode(settings.window_size)
clock = pygame.time.Clock()

draw_options = pymunk.pygame_util.DrawOptions(screen)
pymunk.pygame_util.positive_y_is_up = False


## Init physics (pymunk)
physics.init()

## Add a player
player = Player(pygame.math.Vector2(200, 200), size=30)
EntityManager.add(player)

## Make camera follow player
camera.main.follow(player)

## Add enemies
for i in range(5):
    enemy = Enemy(pygame.math.Vector2(100, 100), size=10, speed=200)
    EntityManager.add(enemy)

## Add a tile
tile = Tile(pygame.math.Vector2(300, 300))
EntityManager.add(tile)

def handle_inputs():
    InputManager.set_frame_pressed()
    InputManager.set_frame_events()

    if InputManager.get_action_down(InputManager.Actions.DEBUG):
        settings.debug = not settings.debug

    for event in InputManager.events:
        if event.type == pygame.QUIT: 
            sys.exit()
                

def update():
    dt = clock.tick(settings.fps) / 1000 # in seconds

    camera.main.update(dt)

    physics.update()
    
    for entity in EntityManager.entities:
        entity.update(dt)


def render():
    screen.fill((0, 0, 0))

    camera.main.render(screen)

    for entity in EntityManager.entities:
        if camera.main.is_visible(entity):
            entity.render(screen)

    if settings.debug:
        physics.space.debug_draw(draw_options)

    pygame.display.flip()