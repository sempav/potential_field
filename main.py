#! /usr/bin/env python2


import math
import pygame

from common import engine, vector, potential, obstacle
from common.vector import Point, Vector, length, normalize
from common.graphics import Graphics
from common.field import Field
from common.bot import Bot
from common import behavior


FRAMERATE = 60
FRAMES_PER_BOT_UPDATE = 1

FIELD_W = 10.0
FIELD_H = 10.0
QUANT_W = 1000
QUANT_H = 1000

MOVEMENT_LAW = engine.Movement.Speed

TRAP = False


def main():
    size = (1910, 1040)
    field = Field((0.01 * size[0], 0.01 * size[1]), size)
    graph = Graphics(field, size)
    eng = engine.Engine(field)

    eng.bots.append(Bot(pos=( 5.0,  0.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-3.0, -1.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-5.0,  0.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-5.0,  1.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-6.0,  0.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-6.0, -1.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-7.0,  0.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))
    eng.bots.append(Bot(pos=(-7.0,  1.0), vel=(0.0, 0.0), behavior=behavior.Basic(movement=MOVEMENT_LAW)))

    eng.targets.append(Point(4.5, 1.0))

    if TRAP:
        eng.obstacles.extend(obstacle.polygon_to_obstacles([Point(0, -3),
                                                            Point(3, -3),
                                                            Point(3,  3),
                                                            Point(0,  3),
                                                            Point(0,  2),
                                                            Point(2,  2),
                                                            Point(2, -2),
                                                            Point(0, -2)]))
    else:
        eng.obstacles.append(obstacle.create_obstacle_circle(Point(1.25, 0.5), 1.1))
        eng.obstacles.append(obstacle.create_obstacle_circle(Point(-1.25, 0.0), 0.2))

    finished = False
    clock = pygame.time.Clock()
    iter_counter = 1
    while not finished:
        delta_time = clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        iter_counter += 1
        if iter_counter % FRAMES_PER_BOT_UPDATE == 0:
            eng.update_bots()
        eng.update_physics(delta_time)
        time = 0.001 * pygame.time.get_ticks()
        #eng.targets[0] = Point(math.cos(2 * time),
        #                       math.sin(2 * time))
        graph.render(bots = eng.bots,
                     obstacles = eng.obstacles,
                     targets = eng.targets)

    pygame.quit()


if __name__ == "__main__":
    main()
