from engine.bot import BOT_VEL_CAP, BOT_ACCEL_CAP, BOT_RADIUS
from engine.vector import Point, Vector, signed_angle, rotate, length, normalize
from math import pi, copysign, sin, cos
from engine.graphics import draw_circle, draw_line, BOT_COLOR

MIN_ROTATION_ANGLE = 0.01 * pi
ROTATION_GAIN = 1.0 # !before changing check abs_vel *= cos(ang) line
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

        # don't move forward when doing a sharp turn;
        # this seems sensible and also prevents bots from
        # slamming into obstacles when trying to move away
        #
        # !this only makes sense with ROTATION_GAIN = 1.0!
        abs_vel *= cos(signed_angle(desired_vel, self.dir))
        if abs_vel < 0:
            abs_vel = 0

        # these are the velocities wheels would get
        # if they didn't have to accelerate smoothly
        target_lvel = abs_vel - 0.5 * self.width * ang
        target_rvel = abs_vel + 0.5 * self.width * ang
        #self.lvel = target_lvel
        #self.rvel = target_rvel
        if abs(self.lvel - target_lvel) < delta_time * BOT_ACCEL_CAP:
            self.lvel = target_lvel
        else:
            self.lvel += copysign(BOT_ACCEL_CAP, target_lvel - self.lvel) * delta_time
        if abs(self.rvel - target_rvel) < delta_time * BOT_ACCEL_CAP:
            self.rvel = target_rvel
        else:
            self.rvel += copysign(BOT_ACCEL_CAP, target_rvel - self.rvel) * delta_time
        # cap velocity
        v = max(self.lvel, self.rvel)
        if v > self.max_vel:
            self.lvel *= self.max_vel / v
            self.rvel *= self.max_vel / v


    def update_state(self, delta_time):
        self.pos += delta_time * self.vel
        self.dir = rotate(self.dir, delta_time * self.rot_vel)


    def draw(self, screen, field):
        draw_circle(screen, field, BOT_COLOR,
                           self.pos,
                           self.radius, 1)
        top_angle = 40 * pi / 180
        x = self.radius * sin(top_angle)
        y = self.radius * cos(top_angle)
        ang = signed_angle(Vector(0.0, 1.0), self.dir)
        pa = self.pos + rotate(Vector(-x, -y), ang)
        pb = self.pos + rotate(Vector( x, -y), ang)
        pc = self.pos + rotate(Vector(0.0, self.radius), ang)
        draw_line(screen, field, BOT_COLOR, pa, pb, 1)
        draw_line(screen, field, BOT_COLOR, pa, pc, 1)
        draw_line(screen, field, BOT_COLOR, pb, pc, 1)
