from vector import Vector, Point, dist, length, normalize
from engine import Movement


BOT_RADIUS = 0.3
BOT_ACCEL_CAP = 1e-5
BOT_VEL_CAP = 1e-3

OBSTACLE_SENSING_DISTANCE = 5 * BOT_RADIUS
KNOW_BOT_POSITIONS = False


class BehaviorBase():
    """
    "Abstract" base class for movement logic.

    Any concrete subclass must redefine calc_desired_velocity.
    """

    def calc_desired_velocity(self, bots, obstacles, targets):
        raise NotImplemented


    def update_vel(self, bots, obstacles, targets):
        self.vel = self.calc_desired_velocity(bots, obstacles, targets)


    def sync_to_real(self, real):
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
    def __init__(self, pos, vel, behavior):
        self.virtual = behavior
        self.real = PhysicalBot(Point(*pos), Vector(*vel))
        self.virtual.sync_to_real(self.real)
