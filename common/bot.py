from vector import Vector, Point
from engine import Movement
import potential


FORCE_SENSITIVITY = 1e-3
BOT_RADIUS = 0.3


class Bot():
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
            impulse = -FORCE_SENSITIVITY * potential.gradient(inter.pos,
                                                              self.pos,
                                                              self.radius + inter.radius)
            delta_v = impulse
            vel = Vector(vel.x + delta_v.x,
                         vel.y + delta_v.y)
            if self.movement == Movement.Dir:
                if length(vel) > 0:
                    vel = vector.normalize(vel)
                    vel *= self.velocity_cap
        return vel


def center_of_mass(bots):
    avg = Vector(0.0, 0.0)
    for bot in bots:
        avg += bot.pos
    avg = avg / (1.0 * len(self.bots))
    return avg
