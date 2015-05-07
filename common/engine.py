import potential
import vector
from vector import Point, Vector, length, normalize

import enum


class Movement(enum.Enum):
    Accel = 1
    Speed = 2
    Dir = 3


class Engine():

    def __init__(self, field, velocity_cap, border_reflect = False):
        self.field = field

        self.velocity_cap = velocity_cap
        self.border_reflect = border_reflect

        self.bots = []
        self.obstacles = []
        self.targets = []


    def border_reflect_bots(self):
        for i, bot in enumerate(self.bots):
            pos = bot.pos
            vel = bot.vel
            abs_vel = Vector(abs(vel.x), abs(vel.y))
            if pos.x < -1:
                self.bots[i].pos = Vector(-1, pos.y)
                self.bots[i].vel = Vector(abs_vel.x, vel.y)
            if pos.x > 1:
                self.bots[i].pos = Vector(1, pos.y)
                self.bots[i].vel = Vector(-abs_vel.x, vel.y)
            if pos.y < -1:
                self.bots[i].pos = Vector(pos.x, -1)
                self.bots[i].vel = Vector(vel.x, abs_vel.y)
            if pos.y > 1:
                self.bots[i].pos = Vector(pos.x, 1)
                self.bots[i].vel = Vector(vel.x, -abs_vel.y)


    def cap_bot_velocities(self, cap):
        for i in xrange(len(self.bots)):
            vel = self.bots[i].vel
            if vector.length(vel) > cap:
                coeff = vector.length(vel) / cap
                self.bots[i].vel = Vector(vel.x / coeff, vel.y / coeff)


    def update(self, delta_time):
        for i, bot in enumerate(self.bots):
            bot.vel = bot.calc_desired_velocity(self.bots, self.obstacles, self.targets)

        if self.border_reflect:
            self.border_reflect_bots()

        self.cap_bot_velocities(self.velocity_cap)

        for i in xrange(len(self.bots)):
            self.bots[i].pos = Point(self.bots[i].pos.x + self.bots[i].vel.x * delta_time,
                                     self.bots[i].pos.y + self.bots[i].vel.y * delta_time)


