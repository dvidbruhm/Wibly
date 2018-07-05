import pymunk

import settings

space = None

def init():
    global space
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.collision_slop = 0.0001

    #space.damping = 0

def add_circle_body(position, radius, mass=10, body_type="static"):
    global space
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position

    if body_type == "static":
        body.body_type = pymunk.Body.STATIC
    elif body_type == "dynamic":
        body.body_type = pymunk.Body.DYNAMIC
    elif body_type == "kinematic":
        body.body_type = pymunk.Body.KINEMATIC

    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return body

def add_polygon_body(points, mass=10, body_type="static"):
    global space

    moment = 1.0
    body = pymunk.Body(mass, moment)

    if body_type == "static":
        body.body_type = pymunk.Body.STATIC
    elif body_type == "dynamic":
        body.body_type = pymunk.Body.DYNAMIC
    elif body_type == "kinematic":
        body.body_type = pymunk.Body.KINEMATIC

    shape = pymunk.Poly(body, points)
    space.add(body, shape)
    return body

def update():
    global space
    space.step(1.0)