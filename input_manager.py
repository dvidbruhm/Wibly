import pygame
from enum import Enum

class Actions(Enum):
    QUIT = 'quit'
    MOVEUP = 'moveup'
    MOVEDOWN = 'moveudown'
    MOVELEFT = 'moveleft'
    MOVERIGHT = 'moveright'

key_bindings = {
    Actions.QUIT: pygame.K_ESCAPE,
    Actions.MOVEUP : pygame.K_w,
    Actions.MOVEDOWN : pygame.K_s,
    Actions.MOVELEFT : pygame.K_a,
    Actions.MOVERIGHT : pygame.K_d
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

    for event in events:
        if event.type == pygame.KEYDOWN:
            if key_bindings[action] == event.key:
                return True

    return False
