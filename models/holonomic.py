from engine.bot import BOT_VEL_CAP, BOT_ACCEL_CAP, BOT_RADIUS
from engine.vector import Point, Vector, length, normalize
from engine.graphics import draw_circle, BOT_COLOR

class HolonomicModel(object):
    def __init__(self, pos = (0.0, 0.0), dir = (1.0, 0.0), vel = 0.0,
                       max_vel = BOT_VEL_CAP,
                       max_accel = BOT_ACCEL_CAP,
                       radius = BOT_RADIUS):
        self.pos = Point(*pos)
        self.vel = vel * Vector(*dir)
        self.max_vel = max_vel
        self.max_accel = max_accel
        self.radius = radius


    @property
    def dir(self):
        try:
            return normalize(self.vel)
        except ZeroDivisionError:
            return Vector(1.0, 0.0)


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


    def draw(self, screen, field):
        draw_circle(screen, field, BOT_COLOR,
                           self.pos,
                           self.radius, 1)
