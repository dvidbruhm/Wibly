import pygame
from enum import Enum

class Actions(Enum):
    QUIT = 'quit'
    DEBUG = 'debug'
    MOVEUP = 'moveup'
    MOVEDOWN = 'moveudown'
    MOVELEFT = 'moveleft'
    MOVERIGHT = 'moveright'
    PUNCH = 'punch'

key_bindings = {
    Actions.QUIT: pygame.K_ESCAPE,
    Actions.DEBUG: pygame.K_TAB,
    Actions.MOVEUP : pygame.K_w,
    Actions.MOVEDOWN : pygame.K_s,
    Actions.MOVELEFT : pygame.K_a,
    Actions.MOVERIGHT : pygame.K_d,
    Actions.PUNCH : pygame.K_SPACE
}

events = []
pressed = {}

def set_frame_pressed():
    global pressed
    pressed = pygame.key.get_pressed()

def set_frame_events():
    global events
    events = pygame.event.get()

def get_action(action):
    return pressed[key_bindings[action]]

def get_action_down(action):
    global events
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == key_bindings[action]:
                return True
    return False