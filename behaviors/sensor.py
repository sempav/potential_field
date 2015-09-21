from vector import Vector, normalize, dist
from shapes import Ray, first_intersection
from math import cos, sin

class Sensor():
    def __init__(self, angle, bot_radius, max_distance):
        self.angle = angle
        self.bot_radius = bot_radius
        self.max_distance = max_distance


    def get_ray(self, bot_pos, bot_angle):
        ang = self.angle + bot_angle
        c = cos(ang)
        s = sin(ang)
        #  c s
        # -s c
        dir = Vector(0, self.bot_radius)
        dir = Vector( dir.x * c + dir.y * s,
                     -dir.x * s + dir.y * c)
        dir = normalize(dir)
        return Ray(bot_pos + dir * self.bot_radius, dir)


    # returns max_distance if there are no
    # intersections closer than max_distance
    def get_distance(self, bot_pos, bot_angle, obstacles):
        ray = self.get_ray(bot_pos, bot_angle)
        p = first_intersection(ray, obstacles)
        if p is None:
            return self.max_distance
        else:
            return min(self.max_distance, dist(ray.orig, p))
