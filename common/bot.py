from vector import Vector, Point, dist, length, normalize
from engine import Movement
import potential


FORCE_SENSITIVITY = 1e-4
BOT_RADIUS = 0.3
BOT_ACCEL_CAP = 1e-3
BOT_VEL_CAP = 1e+3


class VirtualBot():
    def __init__(self, pos = (0, 0), vel = (0, 0), movement = Movement.Accel):
        self.pos = Point(*pos)
        self.vel = Vector(*vel)
        self.movement = movement
        self.radius = BOT_RADIUS

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

        for target in targets:
            impulse = FORCE_SENSITIVITY * potential.gradient(potential.quadratic,
                                             lambda pos: dist(target, pos),
                                             self.pos,
                                             target - self.pos,
                                             0)
            vel += impulse

        for obstacle in obstacles:
            impulse = -FORCE_SENSITIVITY * potential.gradient(potential.inverse_quadratic,
                                              obstacle.distance,
                                              self.pos,
                                              obstacle.center - self.pos,
                                              self.radius)
            vel += impulse

        if self.movement == Movement.Dir:
            if length(vel) > 0:
                vel = normalize(vel)
        return vel


    def update_vel(self, bots, obstacles, targets):
        self.vel = self.calc_desired_velocity(bots, obstacles, targets)


    def sync_to_reality(self, real):
        self.pos = real.pos
        self.vel = real.vel


class PhysicalBot():
    def __init__(self, pos = (0, 0), vel = (0, 0), max_vel = BOT_VEL_CAP,
                                                   max_accel = BOT_ACCEL_CAP):
        self.pos = Point(*pos)
        self.vel = Vector(*vel)
        self.max_vel = max_vel
        self.max_accel = max_accel


    def update_vel(self, delta_time, desired_vel):
        dv = desired_vel - self.vel
        if length(dv) < self.max_accel * delta_time:
            self.vel = desired_vel
        else:
            self.vel += normalize(dv) * self.max_accel * delta_time

        if length(self.vel) > self.max_vel:
            self.vel = self.max_vel * normalize(self.vel)


class Bot():
    def __init__(self, pos = (0, 0), vel = (0, 0), movement = Movement.Accel):
        self.virtual = VirtualBot(pos, vel, movement)
        self.real = PhysicalBot(pos, vel)
