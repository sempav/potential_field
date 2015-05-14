from functools import partial

from bot import BehaviorBase, BOT_RADIUS, OBSTACLE_SENSING_DISTANCE, KNOW_BOT_POSITIONS
from engine import Movement
import potential
from vector import Vector, length, normalize, dist


FORCE_SENSITIVITY = 1e-4


class Basic(BehaviorBase):
    def __init__(self, movement = Movement.Accel,
                 obstacle_sensing_distance = OBSTACLE_SENSING_DISTANCE):
        self.movement = movement
        self.radius = BOT_RADIUS
        self.obstacle_sensing_distance = obstacle_sensing_distance


    def calc_desired_velocity(self, bots, obstacles, targets):
        vel = self.vel
        if self.movement != Movement.Accel:
            vel = Vector(0, 0)
        for inter in bots:
            if (not KNOW_BOT_POSITIONS) and dist(inter.real.pos, self.pos) > self.obstacle_sensing_distance:
                continue
            force = -potential.gradient(partial(potential.morse, d0=2 * BOT_RADIUS, k=2.5, a=5.0),
                                              lambda pos: dist(inter.real.pos, pos),
                                              self.pos,
                                              inter.real.pos - self.pos,
                                              self.radius + inter.virtual.radius)
            vel += FORCE_SENSITIVITY * force

        for target in targets:
            force = -potential.gradient(partial(potential.linear, k=2.0),
                                             lambda pos: dist(target, pos),
                                             self.pos,
                                             target - self.pos,
                                             0)
            vel += FORCE_SENSITIVITY * force

        for obstacle in obstacles:
            if obstacle.distance(self.pos) <= self.obstacle_sensing_distance:
                force = -potential.gradient(partial(potential.inverse_quadratic, k=0.5),
                                                  obstacle.distance,
                                                  self.pos,
                                                  obstacle.repulsion_dir(self.pos),
                                                  self.radius)
                vel += FORCE_SENSITIVITY * force

        if self.movement == Movement.Dir:
            if length(vel) > 0:
                vel = normalize(vel)
        return vel


class Sensor(BehaviorBase):
    def calc_desired_velocity(self, bots, obstacles, targets):
        vel = self.vel
        if self.movement != Movement.Accel:
            vel = Vector(0, 0)

        for inter in bots:
            impulse = -FORCE_SENSITIVITY * potential.gradient(potential.morse,
                                              lambda pos: dist(inter.real.pos, pos),
                                              self.pos,
                                              inter.real.pos - self.pos,
                                              self.radius + inter.virtual.radius)
            vel += impulse

        for obstacle in obstacles:
            pass

        for target in targets:
            impulse = FORCE_SENSITIVITY * potential.gradient(potential.quadratic,
                                             lambda pos: dist(target, pos),
                                             self.pos,
                                             target - self.pos,
                                             0)
            vel += impulse

        if self.movement == Movement.Dir:
            if length(vel) > 0:
                vel = normalize(vel)
        return vel
