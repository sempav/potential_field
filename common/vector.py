import collections
from math import sqrt
import numbers


def length(v):
    return sqrt(v[0] * v[0] + v[1] * v[1])

def dist(a, b):
    return length( (a[0] - b[0], a[1] - b[1]) )

def normalize(v):
    return type(v)(v[0] / length(v), v[1] / length(v))

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


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

Vector.__add__ = __add__
Vector.__sub__ = __sub__
Vector.__neg__ = __neg__
Vector.__mul__ = __mul__
Vector.__rmul__ = __rmul__

