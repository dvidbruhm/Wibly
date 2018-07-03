import pygame
import sys

import input_manager as InputManager
import entity_manager as EntityManager
import settings
import camera

from player import Player
from enemy import Enemy
from tile import Tile

pygame.init()
screen = pygame.display.set_mode(settings.window_size)
clock = pygame.time.Clock()

player = Player(pygame.math.Vector2(200, 200), size=30)
EntityManager.add(player)

camera.main.follow(player)

for i in range(20):
    enemy = Enemy(pygame.math.Vector2(100, 100), size=20)
    EntityManager.add(enemy)

tile = Tile(pygame.math.Vector2(300, 300))
EntityManager.add(tile)

def handle_inputs():
    InputManager.set_frame_pressed()
    InputManager.set_frame_events()

    for event in InputManager.events:
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == InputManager.key_bindings[InputManager.Actions.DEBUG]:
                settings.debug = not settings.debug

def update():
    dt = clock.tick(30) / 1000 # in seconds

    camera.main.update(dt)

    for entity in EntityManager.entities:
        entity.update(dt)

def render():
    screen.fill((0, 0, 0))

    camera.main.render(screen)

    for entity in EntityManager.entities:
        if camera.main.is_visible(entity):
            entity.render(screen)

    pygame.display.flip()