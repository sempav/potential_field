from bot import BOT_VEL_CAP, BOT_ACCEL_CAP
from vector import Point, Vector, length, normalize

class HolonomicModel():
    def __init__(self, pos = (0.0, 0.0), vel = (0.0, 0.0),
                       max_vel = BOT_VEL_CAP,
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


    def update_state(self, delta_time):
        self.pos += self.vel * delta_time
