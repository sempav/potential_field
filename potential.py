import math

from vector import Vector, dist, normalize


class morse():
    def __init__(self, r0, k, a):
        self.r0 = r0
        self.k = k
        self.a = a

    def __call__(self, r):
        r0 = self.r0
        k = self.k
        a = self.a
        return k * (1 - math.exp(-a * (r - r0)))**2

    def derivative(self, r):
        r0 = self.r0
        k = self.k
        a = self.a
        return 2 * k * (1 - math.exp(-a * (r - r0))) * a * math.exp(-a * (r - r0))


class linear():
    def __init__(self, k=1.0):
        self.k = k

    def __call__(self, r):
        return self.k * r

    def derivative(self, r):
        return self.k


class quadratic():
    def __init__(self, k=1.0):
        self.k = k

    def __call__(self, r):
        return self.k * r * r

    def derivative(self, r):
        return 2 * self.k * r


class inverse_quadratic():
    def __init__(self, k=1.0):
        self.k = k

    def __call__(self, r):
        return self.k / (r * r)

    def derivative(self, r):
        return -2 * self.k / (r * r * r)


def numerical_gradient(distance_potential, dist_fun, pos, direction, thickness):
    eps = 1e-4
    here  = distance_potential(dist_fun(pos) - thickness)
    there = distance_potential(dist_fun(pos + eps * direction) - thickness)
    coeff = (there - here) / eps
    try:
        return normalize(direction) * coeff
    except ZeroDivisionError:
        return Vector(0.0, 0.0)


def gradient(distance_potential, dist, direction, thickness):
    # use sympy, perhaps?
    coeff = distance_potential.derivative(dist - thickness)
    try:
        return normalize(direction) * coeff
    except ZeroDivisionError:
        return Vector(0.0, 0.0)
