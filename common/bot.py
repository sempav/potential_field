from vector import Vector, Point, dist, length, normalize
from engine import Movement
import potential


FORCE_SENSITIVITY = 1e-4
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
            impulse = -FORCE_SENSITIVITY * potential.gradient(potential.morse,
                                              lambda pos: dist(inter.pos, pos),
                                              self.pos,
                                              inter.pos - self.pos,
                                              self.radius + inter.radius)
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


def center_of_mass(bots):
    avg = Vector(0.0, 0.0)
    for bot in bots:
        avg += bot.pos
    avg = avg / (1.0 * len(self.bots))
    return avg
