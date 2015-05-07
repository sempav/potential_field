import math

from vector import dist


def morse(r):
    d0 = 1.5
    k = 1.0
    a = 1.0
    return k * (1 - math.exp(-a * (r - d0)))**2


def quadratic(r):
    return -0.5 * r


def inverse_quadratic(r):
    return 0.5 / (r * r)


def gradient(distance_potential, dist_fun, pos, direction, thickness):
    eps = 1e-4
    here  = distance_potential(dist_fun(pos) - thickness)
    there = distance_potential(dist_fun(pos + eps * direction) - thickness)
    coeff = (there - here) / eps
    return direction * coeff
