import pygame

import camera
import settings

import numpy as np


PI = 3.1415

class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

def world_to_screen(input):
    center_window = [a / 2 for a in settings.window_size]

    if isinstance(input, pygame.math.Vector2) or isinstance(input, tuple):
        screen_pos = tuple([x + y for x, y in zip(vec_to_pos(input - camera.main.position), vec_to_pos(center_window))])
        return screen_pos
    elif isinstance(input, pygame.Rect):
        rect = pygame.Rect(tuple([x - y for x, y in zip(vec_to_pos(input), vec_to_pos(camera.main.position))]), (input.w, input.h))
        rect.x += center_window[0]
        rect.y += center_window[1]
        return rect

def vec_to_pos(vector):
    return (int(vector[0]), int(vector[1]))

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) * 180 / 3.1416
    return angle
def lerp(a, b, time):
    if time > 1 or time < 0:
        raise Exception("Value has to be between 0 and 1 for lerp.")
    return a + time * (b - a)

def lerp_angle(a, b, t):
    if abs(a-b) >= 180:
        if a > b:
            a = normalize_angle(a) - 2.0 * 180
        else:
            b = normalize_angle(b) - 2.0 * 180
    return lerp(a, b, t)

def normalize_angle(x):
    return ((x + 180) % (2.0*180)) - 180

def slerp(a, b, time):
    angle = angle_between(np.array(a), np.array(b))
    if angle >= 179:
        a.x += 0.01
        a.y += 0.01
        a = a.normalize()
    return a.slerp(b, time)

def tuple_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def tuple_mul(a, b):
    return (a[0] * b[0], a[1] * b[1])

