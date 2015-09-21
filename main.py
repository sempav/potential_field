#! /usr/bin/env python2


import math
import pygame
import os

import engine, vector, potential, obstacle
import behaviors
import models
from vector import Point, Vector, length, normalize
from graphics import Graphics
from field import Field
from bot import Bot


FRAMERATE = 60
FRAMES_PER_BOT_UPDATE = 1


def reset(eng, trap, group, movement=engine.Movement.Speed):
    eng.bots = []
    eng.obstacles = []
    eng.targets = []

    if group:
        eng.bots.append(Bot(models.HolonomicModel(pos=( 5.0,  0.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(models.HolonomicModel(pos=(-3.0, -1.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(models.HolonomicModel(pos=(-5.0,  0.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(models.HolonomicModel(pos=(-5.0,  1.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(models.HolonomicModel(pos=(-6.0,  0.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(models.HolonomicModel(pos=(-6.0, -1.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(models.HolonomicModel(pos=(-7.0,  0.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))
    eng.bots.append(Bot(models.HolonomicModel(pos=(-7.0,  1.0), vel=(0.0, 0.0)), behavior=behaviors.SensorBased(movement)))

    if trap:
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

    eng.targets.append(Point(4.5, 1.0))


def show_state(movement):
    if movement == engine.Movement.Accel:
        return "Acceleration mode"
    elif movement == engine.Movement.Speed:
        return "Velocity mode"
    else:
        return "Direction mode"


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1,20)

    pygame.init()

    #font = pygame.font.Font(None, 30)
    font = pygame.font.SysFont("Arial", 25)

    #pygame.display.init()
    info = pygame.display.Info()
    size = (info.current_w - 1, info.current_h - 20)
    field = Field((0.01 * size[0], 0.01 * size[1]), size)
    graph = Graphics(field, size)
    eng = engine.Engine(field)

    cur_group = True
    cur_trap = False
    cur_movement = engine.Movement.Speed
    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)

    finished = False
    clock = pygame.time.Clock()
    iter_counter = 1

    while not finished:
        delta_time = clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cur_movement = engine.Movement.Accel
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)
                elif event.key == pygame.K_2:
                    cur_movement = engine.Movement.Speed
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)
                elif event.key == pygame.K_3:
                    cur_movement = engine.Movement.Dir
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)
                elif event.key == pygame.K_q:
                    cur_trap = False
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)
                elif event.key == pygame.K_w:
                    cur_trap = True
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)
                elif event.key == pygame.K_a:
                    cur_group = True
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)
                elif event.key == pygame.K_s:
                    cur_group = False
                    reset(eng, trap=cur_trap, group=cur_group, movement=cur_movement)

        iter_counter += 1
        if iter_counter % FRAMES_PER_BOT_UPDATE == 0:
            eng.update_bots()
        eng.update_physics(delta_time)

        mouse_pos = pygame.mouse.get_pos()
        eng.targets[0] = field.screen_to_field(mouse_pos)
        #time = 0.001 * pygame.time.get_ticks()
        #eng.targets[0] = Point(math.cos(2 * time) + 2 * math.sin(time),
        #                       math.sin(2 * time))

        graph.render(bots = eng.bots,
                     obstacles = eng.obstacles,
                     targets = eng.targets)

        text = show_state(cur_movement)
        ren = font.render(text, 0, (255, 255, 255))
        text_size = font.size(text)
        graph.screen.blit(ren, (30, graph.size[1] - text_size[1]))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
