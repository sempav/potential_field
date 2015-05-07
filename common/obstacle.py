import pygame 

from graphics import OBSTACLE_COLOR
from vector import Vector, Point, dist

class Obstacle():
    def __init__(self, distance_field, draw_fun):
        self.distance = distance_field
        self.draw = draw_fun

def create_obstacle_circle(center, radius):
    def draw_circle(screen, field):
        pygame.draw.circle(screen, OBSTACLE_COLOR,
                           field.fit_on_screen(center),
                           field.scale(radius), 1)

    o = Obstacle(lambda r: dist(r, center) - radius,
                 draw_circle)
    o.center = center
    return o
