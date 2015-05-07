#! /usr/bin/env python2


import math
import pygame

from common import engine, vector, potential
from common.vector import Point, Vector, length, normalize
from common.graphics import Graphics
from common.field import Field
from common.bot import Bot


FRAMERATE = 40

BORDER_REFLECT = False
VELOCITY_CAP = 0.001

FIELD_W = 10.0
FIELD_H = 10.0
QUANT_W = 1000
QUANT_H = 1000

MOVEMENT_LAW = engine.Movement.Speed


def main():
    size = (1024, 768)
    #field = Field((10.0, 10.0))
    field = Field((0.01 * size[0], 0.01 * size[1]))
    graph = Graphics(field, size)
    eng = engine.Engine(field, VELOCITY_CAP,
                               BORDER_REFLECT)

    eng.bots.append(Bot(pos = ( 0.0,  0.1), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = ( 1.0,  0.2), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = ( 2.0,  0.7), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-3.0,  0.5), vel = (0.0, 0.0), movement = MOVEMENT_LAW))

    finished = False
    clock = pygame.time.Clock()
    while not finished:
        delta_time = clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True;
        eng.update(delta_time)
        graph.render(eng.bots)
    pygame.quit()


if __name__ == "__main__":
    main()
