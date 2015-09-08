import pygame 
from functools import partial
from itertools import starmap

import shapes
from graphics import OBSTACLE_COLOR
from vector import Vector, Point, dist, normalize, dot, cross

class Obstacle():
    # distance_field takes a Point and returns distance to the obstacle
    # repulsion_field takes a Point and returns direction of the gradient of distance_field
    def __init__(self, distance_field, repulsion_field, _shape):
        self.distance = distance_field
        self.repulsion_dir = repulsion_field
        self.shape = _shape


    def draw(self, screen, field):
        self.shape.draw(screen, field, OBSTACLE_COLOR)


    def intersect(self, ray):
        return self.shape.intersect(ray)


def create_obstacle_circle(center, radius):
    o = Obstacle(lambda r: dist(r, center) - radius,
                 lambda r: normalize(r - center),
                 shapes.Circle(center, radius))
    o.center = center
    return o


def edges(vertices):
    assert(len(vertices) > 1)
    prev = None
    for cur in vertices:
        if prev is not None:
            yield (prev, cur)
        prev = cur
    yield (prev, vertices[0])


def draw_polygon(screen, field, vertices):
    for u,v in edges(vertices):
        pygame.draw.line(screen, OBSTACLE_COLOR,
                         field.fit_on_screen(u),
                         field.fit_on_screen(v))


def distance_to_segment(point, a, b):
    if dot(b - a, point - a) <= 0 or dot(a - b, point - b) <= 0:
        return min(dist(point, a), dist(point, b))
    return abs(cross(point - a, normalize(b - a)))


def dir_from_segment(point, a, b):
    if dot(b - a, point - a) <= 0:
        return normalize(point - a)
    if dot(a - b, point - b) <= 0:
        return normalize(point - b)
    normal = normalize(b - a)
    normal = Vector(-normal.y, normal.x)
    if dot(normal, point - a) < 0:
        normal = -normal
    assert(distance_to_segment(point, a, b) < distance_to_segment(point + normal, a, b))
    return normal


def distance_to_polygon(point, vertices):
    return min(map(partial(distance_to_segment, point=point), edges(vertices)))


def dir_from_polygon(point, vertices):
    _, u, v = min((distance_to_segment(point, u, v),u,v) for (u, v) in edges(vertices))
    return dir_from_segment(point, u, v)


def create_obstacle_segment(a, b):
    o = Obstacle(partial(distance_to_segment, a=a, b=b),
                 partial(dir_from_segment, a=a, b=b),
                 shapes.Segment(a, b))
    o.center = 0.5 * (a + b)
    return o


def polygon_to_obstacles(vertices):
    return starmap(create_obstacle_segment, edges(vertices))

def create_obstacle_polygon(vertices):
    o = Obstacle(partial(distance_to_polygon, vertices=vertices),
                 partial(dir_from_polygon, vertices=vertices),
                 shapes.Polygon(vertices))
