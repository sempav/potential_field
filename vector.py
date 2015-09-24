import collections
from math import sqrt, atan2, sin, cos
import numbers

# precision of geometric operations, used in tests
geom_eps = 1e-5
# this should be -lg(geom_eps); used in tests
geom_places = 5


def length(v):
    return sqrt(v[0] * v[0] + v[1] * v[1])

def dist(a, b):
    return length( (a[0] - b[0], a[1] - b[1]) )

def normalize(v):
    return Vector(v[0] / length(v), v[1] / length(v))

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

# returns absolute value of the cross product
def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

# returns *absolute* value of the angle between two vectors
def angle(a, b):
    return abs(signed_angle(a, b))

# returns signed angle between two vectors
def signed_angle(a, b):
    return atan2(cross(a, b), dot(a, b))

def rotate(v, ang):
    c = cos(ang)
    s = sin(ang)
    return Vector(v.x * c - v.y * s,
                  v.x * s + v.y * c)

# define a vector class with proper operations

Vector = collections.namedtuple('Vector', ['x', 'y'])
Point = Vector

def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)

def __sub__(self, other):
    return Vector(self.x - other.x, self.y - other.y)

def __neg__(self):
    return Vector(-self.x, -self.y)

def __mul__(self, other):
    if isinstance(other, numbers.Number):
        return Vector(other * self.x, other * self.y)
    else:
        return NotImplemented

def __rmul__(self, other):
    return __mul__(self, other)

def __div__(self, other):
    if isinstance(other, numbers.Number):
        return Vector(self.x / other, self.y / other)
    else:
        return NotImplemented

def __eq__(self, other):
    return length(self - other) < geom_eps

def __ne__(self, other):
    return not self.__eq__(other)

Vector.__add__ = __add__
Vector.__sub__ = __sub__
Vector.__neg__ = __neg__
Vector.__mul__ = __mul__
Vector.__rmul__ = __rmul__
Vector.__div__ = __div__
Vector.__eq__ = __eq__
Vector.__ne__ = __ne__

