from bot import BOT_VEL_CAP, BOT_ACCEL_CAP, BOT_RADIUS
from vector import Point, Vector, signed_angle, rotate, length, normalize
from math import pi, copysign

MIN_ROTATION_ANGLE = 0.01 * pi
#ROTATION_RATE = pi * 1e-3
ROTATION_GAIN = 0.001
MAX_VEL_ANGLE = pi / 3

class DifferentialModel():
    def __init__(self, pos, dir, vel = 0.0,
                       max_vel = BOT_VEL_CAP,
                       max_accel = BOT_ACCEL_CAP,
                       radius = BOT_RADIUS):
        self.pos = Point(*pos)
        self.dir = normalize(dir)
        self.lvel = vel
        self.rvel = vel
        self.max_vel = max_vel
        self.max_accel = max_accel
        self.radius = radius
        self.width = 2.0 * radius


    @property
    def vel(self):
        return self.dir * 0.5 * (self.lvel + self.rvel)

    @property
    def rot_vel(self):
        return (self.rvel - self.lvel) / self.width


    def update_vel(self, delta_time, desired_vel):
        ang = signed_angle(self.dir, desired_vel)
        if abs(ang) < MIN_ROTATION_ANGLE:
            ang = 0.0
        ang = ROTATION_GAIN * ang
        abs_vel = min(length(desired_vel), self.max_vel)
        self.lvel = abs_vel - 0.5 * self.width * ang
        self.rvel = abs_vel + 0.5 * self.width * ang
        # cap velocity
        v = max(self.lvel, self.rvel)
        if v > self.max_vel:
            self.lvel *= self.max_vel / v
            self.rvel *= self.max_vel / v


    def update_state(self, delta_time):
        self.pos += delta_time * self.vel
        self.dir = rotate(self.dir, delta_time * self.rot_vel)
