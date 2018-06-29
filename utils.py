import pygame

import camera
import settings

import numpy as np

class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

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
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))