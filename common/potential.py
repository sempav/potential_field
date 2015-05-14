import math

from vector import dist


def morse(r, d0, k, a):
    return k * (1 - math.exp(-a * (r - d0)))**2

def linear(r, k=1.0):
    return k * r

def quadratic(r, k=1.0):
    return k * r * r


def inverse_quadratic(r, k=1.0):
    return k / (r * r)


def gradient(distance_potential, dist_fun, pos, direction, thickness):
    eps = 1e-4
    here  = distance_potential(dist_fun(pos) - thickness)
    there = distance_potential(dist_fun(pos + eps * direction) - thickness)
    coeff = (there - here) / eps
    return direction * coeff
