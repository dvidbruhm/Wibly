import pymunk

import settings

space = None

class Categories:
    OTHER = 0
    PLAYER = 1
    ENEMY = 2
    WALL = 3

def init():
    global space
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.collision_slop = 0.0001

    #space.damping = 0

def add_circle_body(position, radius, mass=10, body_type="static", category=pymunk.ShapeFilter.ALL_CATEGORIES):
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
    shape.filter = pymunk.ShapeFilter(categories=category)
    space.add(body, shape)

    return body

def add_polygon_body(points, mass=10, body_type="static", category=pymunk.ShapeFilter.ALL_CATEGORIES):
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
    shape.filter = pymunk.ShapeFilter(categories=category)
    space.add(body, shape)
    return body
    
def add_segment_body(start, end, mass=10, body_type="static", category=pymunk.ShapeFilter.ALL_CATEGORIES):
    global space

    points = [start, end]
    moment = 1.0
    body = pymunk.Body(mass, moment)

    if body_type == "static":
        body.body_type = pymunk.Body.STATIC
    elif body_type == "dynamic":
        body.body_type = pymunk.Body.DYNAMIC
    elif body_type == "kinematic":
        body.body_type = pymunk.Body.KINEMATIC

    shape = pymunk.Segment(body, start, end, 1)
    shape.filter = pymunk.ShapeFilter(categories=category)
    space.add(body, shape)
    return body

def segment_query_first(start, end, radius, category=pymunk.ShapeFilter.ALL_CATEGORIES):
    global space
    filter = pymunk.ShapeFilter(categories=category)
    return space.segment_query_first(start, end, radius, filter)

def update():
    global space
    space.step(1.0)