#! /usr/bin/env python2


import math
import pygame

from common import engine, vector, potential, obstacle
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
    size = (1910, 1040)
    field = Field((0.01 * size[0], 0.01 * size[1]), size)
    graph = Graphics(field, size)
    eng = engine.Engine(field, VELOCITY_CAP,
                               BORDER_REFLECT)

    eng.bots.append(Bot(pos = ( 3.0,  0.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-3.0, -1.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-5.0,  0.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-5.0, -1.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-6.0,  0.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-6.0, -1.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-7.0,  0.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))
    eng.bots.append(Bot(pos = (-7.0,  1.0), vel = (0.0, 0.0), movement = MOVEMENT_LAW))

    eng.targets.append(Point(4.5, 1.0))

    eng.obstacles.append(obstacle.create_obstacle_circle(Point(1.25, 0.5), 1.1))
    eng.obstacles.append(obstacle.create_obstacle_circle(Point(-1.25, 0.0), 0.2))

    finished = False
    clock = pygame.time.Clock()
    while not finished:
        delta_time = clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True;
        eng.update(delta_time)
        time = 0.001 * pygame.time.get_ticks()
        #eng.targets[0] = Point(math.cos(2 * time),
        #                       math.sin(2 * time))
        graph.render(bots = eng.bots,
                     obstacles = eng.obstacles,
                     targets = eng.targets)

    pygame.quit()


if __name__ == "__main__":
    main()
