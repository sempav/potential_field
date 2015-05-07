import math

from vector import dist

def morse(r):
    d0 = 1.0
    k = 1.0
    a = 1.0
    return k * (1 - math.exp(-a * (r - d0)))**2

def gradient(bot, pos):
    direction = pos - bot
    eps = 10**-4
    here = morse(dist(pos, bot))
    there = morse(dist(pos + eps * direction, bot))
    coeff = (there - here) / eps;
    return direction * coeff;
