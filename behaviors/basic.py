from functools import partial

from base import BehaviorBase
from bot import BOT_RADIUS, \
                MAX_SENSING_DISTANCE, KNOW_BOT_POSITIONS, \
                OBSTACLE_CLEARANCE
from engine import Movement
import potential
from vector import Vector, length, normalize, dist


_FORCE_SENSITIVITY = 5e-4


class Basic(BehaviorBase):
    def __init__(self, movement = Movement.Accel,
                 max_sensing_distance = MAX_SENSING_DISTANCE):
        self.movement = movement
        self.radius = BOT_RADIUS
        self.max_sensing_distance = max_sensing_distance


    def calc_desired_velocity(self, bots, obstacles, targets):
        vel = self.vel
        if self.movement != Movement.Accel:
            vel = Vector(0, 0)
        for inter in bots:
            if (not KNOW_BOT_POSITIONS) and dist(inter.real.pos, self.pos) > self.max_sensing_distance:
                continue
            force = -potential.gradient(potential.morse(r0=2 * BOT_RADIUS, k=2.5, a=4.0),
                                        dist(inter.real.pos, self.pos),
                                        self.pos - inter.real.pos,
                                        self.radius + inter.virtual.radius)
            vel += _FORCE_SENSITIVITY * force

        for target in targets:
            force = -potential.gradient(potential.linear(k=-2.0),
                                        dist(target, self.pos),
                                        target - self.pos,
                                        0)
            vel += _FORCE_SENSITIVITY * force

        for obstacle in obstacles:
            if obstacle.distance(self.pos) <= self.max_sensing_distance:
                force = -potential.gradient(potential.inverse_quadratic(k=1.0),
                                            obstacle.distance(self.pos),
                                            obstacle.repulsion_dir(self.pos),
                                            OBSTACLE_CLEARANCE + self.radius)
                vel += _FORCE_SENSITIVITY * force

        if self.movement == Movement.Dir:
            if length(vel) > 0:
                vel = normalize(vel)
        return vel


    def draw(self, screen, field):
        pass
