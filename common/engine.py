import potential
import vector
from vector import Point, Vector, length, normalize

import enum


class Movement(enum.Enum):
    Accel = 1
    Speed = 2
    Dir = 3


class Engine():

    def __init__(self, field, velocity_cap):
        self.field = field

        self.velocity_cap = velocity_cap

        self.bots = []
        self.obstacles = []
        self.targets = []


    def update_bots(self):
        for bot in self.bots:
            bot.virtual.sync_to_reality(bot.real)

        for bot in self.bots:
            bot.virtual.update_vel(self.bots, self.obstacles, self.targets)


    def update_physics(self, delta_time):
        for bot in self.bots:
            bot.real.update_vel(delta_time, bot.virtual.vel)

        for bot in self.bots:
            bot.real.pos += bot.real.vel * delta_time
