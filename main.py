#! /usr/bin/env python2


import pygame
import os

import engine
import behaviors
import models
from vector import Point
from graphics import Graphics
from field import Field
from bot import Bot
from obstacle_maps import maps


FRAMERATE = 60
FRAMES_PER_BOT_UPDATE = 1


def reset(eng, obstacle_map, group, movement=engine.Movement.Speed, model=models.DifferentialModel):
    eng.bots = []
    eng.obstacles = []
    eng.targets = []

    if group:
        eng.bots.append(Bot(model(pos=( 5.0,  0.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(model(pos=(-3.0, -1.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(model(pos=(-5.0,  0.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(model(pos=(-5.0,  1.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(model(pos=(-6.0,  0.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(model(pos=(-6.0, -1.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
        eng.bots.append(Bot(model(pos=(-7.0,  0.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))
    eng.bots.append(Bot(model(pos=(-7.0,  1.0), dir=(1.0, 0.0), vel=0.0), behavior=behaviors.SensorBased(movement)))

    eng.obstacles = maps[obstacle_map][:]

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
    cur_obstacle_map = 0
    cur_movement = engine.Movement.Speed
    cur_model = models.DifferentialModel
    reset(eng, obstacle_map=cur_obstacle_map, group=cur_group, movement=cur_movement)

    finished = False
    clock = pygame.time.Clock()
    iter_counter = 1

    while not finished:
        delta_time = 0.001 * clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                eng.targets[0] = field.screen_to_field(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    cur_movement = engine.Movement.Accel
                elif event.key == pygame.K_w:
                    cur_movement = engine.Movement.Speed
                elif event.key == pygame.K_e:
                    cur_movement = engine.Movement.Dir
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    cur_obstacle_map = event.key - pygame.K_1
                elif event.key == pygame.K_a:
                    cur_group = True
                elif event.key == pygame.K_s:
                    cur_group = False
                elif event.key == pygame.K_z:
                    cur_model = models.HolonomicModel
                elif event.key == pygame.K_x:
                    cur_model = models.DifferentialModel
                reset(eng, obstacle_map=cur_obstacle_map, group=cur_group, movement=cur_movement, model=cur_model)

        iter_counter += 1
        if iter_counter % FRAMES_PER_BOT_UPDATE == 0:
            eng.update_bots()
        eng.update_physics(delta_time)

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
