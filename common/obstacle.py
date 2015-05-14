import pygame 
from functools import partial
from itertools import starmap

from graphics import OBSTACLE_COLOR
from vector import Vector, Point, dist, normalize, dot, cross

class Obstacle():
    def __init__(self, distance_field, repulsion_field, draw_fun):
        self.distance = distance_field
        self.repulsion_dir = repulsion_field
        self.draw = draw_fun


def draw_circle(screen, field, center, radius):
    pygame.draw.circle(screen, OBSTACLE_COLOR,
                       field.fit_on_screen(center),
                       field.scale(radius), 2)


def edges(vertices):
    assert(len(vertices) > 1)
    prev = None
    for cur in vertices:
        if prev is not None:
            yield (prev, cur)
        prev = cur
    yield (prev, vertices[0])


def draw_segment(screen, field, a, b):
    pygame.draw.line(screen, OBSTACLE_COLOR,
                     field.fit_on_screen(a),
                     field.fit_on_screen(b), 2)


def draw_polygon(screen, field, vertices):
    for u,v in edges(vertices):
        pygame.draw.line(screen, OBSTACLE_COLOR,
                         field.fit_on_screen(u),
                         field.fit_on_screen(v))


def distance_to_segment(point, a, b):
    if dot(b - a, point - a) <= 0 or dot(a - b, point - b) <= 0:
        return min(dist(point, a), dist(point, b))
    return cross(point - a, normalize(b - a))


def dir_from_segment(point, a, b):
    if dot(b - a, point - a) <= 0:
        return normalize(point - a)
    if dot(a - b, point - b) <= 0:
        return normalize(point - b)
    normal = normalize(b - a)
    normal = Vector(-normal.y, normal.x)
    if dot(normal, point - a) < 0:
        normal = -normal
    return normal


def distance_to_polygon(point, vertices):
    return min(map(partial(distance_to_segment, point=point), edges(vertices)))


def create_obstacle_circle(center, radius):
    o = Obstacle(lambda r: dist(r, center) - radius,
                 lambda r: normalize(r - center),
                 partial(draw_circle, center=center, radius=radius))
    o.center = center
    return o


def create_obstacle_segment(a, b):
    o = Obstacle(partial(distance_to_segment, a=a, b=b),
                 partial(dir_from_segment, a=a, b=b),
                 partial(draw_segment, a=a, b=b))
    o.center = 0.5 * (a + b)
    return  o


def polygon_to_obstacles(vertices):
    return starmap(create_obstacle_segment, edges(vertices))
