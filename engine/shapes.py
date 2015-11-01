from graphics import draw_circle, draw_line
from vector import normalize, dot, cross, length, Vector
from math import sqrt

class Ray(object):
    def __init__(self, _orig, _dir):
        self.orig = _orig
        self.dir = normalize(_dir)


    # returns the intersection that is closest to origin
    def intersect(self, shape):
        return shape.intersect(self)


# returns None if the ray doesn't intersect with any objects
def first_intersection(ray, objects):
    # build a list of all intersections and remove Nones
    ps = [e.intersect(ray) for e in objects]
    ps = [p for p in ps if p is not None]
    try:
        # select the point closest to ray.orig
        p = min(ps, key=lambda p: length(p - ray.orig))
        return p
    except ValueError:
        return None


class Circle(object):
    def __init__(self, _center, _radius):
        self.center = _center
        self.radius = _radius


    # returns the intersection that is closest to origin
    def intersect(self, ray):
        oc = self.center - ray.orig
        # let P be projection of C on the line
        # then l = |OP|, h = |CP|
        l = dot(oc, ray.dir)
        h = cross(oc, ray.dir)
        if self.radius < abs(h):
            return None
        q = sqrt(self.radius ** 2 - h ** 2)
        # find t: o + d * t == intersection
        t = l - q
        if t < 0:
            t = l + q
        if t < 0:
            return None
        else:
            return ray.orig + t * ray.dir


    def draw(self, screen, field, color):
        draw_circle(screen, field, color, self.center, self.radius)


class Segment(object):
    def __init__(self, _a, _b):
        self.a = _a
        self.b = _b


    # returns the intersection that is closest to origin
    def intersect(self, ray):
        v1 = ray.orig - self.a
        v2 = self.b - self.a
        v3 = Vector(-ray.dir.y, ray.dir.x)
        if dot(v2, v3) == 0:
            return None
        ts = dot(v1, v3) / dot(v2, v3)
        tr = cross(v2, v1) / dot(v2, v3)
        if tr >= 0.0 and 0.0 <= ts <= 1.0:
            return self.a + v2 * ts
        else:
            return None


    def draw(self, screen, field, color):
        draw_line(screen, field, color, self.a, self.b)


class Polygon(object):
    def __init__(self, _vertices):
        self.edges = []
        prev = _vertices[-1]
        for cur in _vertices:
            self.edges.append(Segment(prev, cur))
            prev = cur


    # returns the intersection that is closest to origin
    def intersect(self, ray):
        return first_intersection(ray, self.edges)


    def draw(self, screen, field, color):
        for e in self.edges:
            e.draw(screen, field, color)
