from vector import Vector, Point
import engine

print dir(engine)

class Bot():
    def __init__(self, pos = (0, 0), vel = (0, 0), movement_law = engine.Movement.Accel):
        self.pos = Point(*pos)
        self.vel = Vector(*vel)
        self.movement_law = movement_law

    def calc_desired_velocity(self, bots, obstacles):
        vel = self.vel
        if self.movement_law != Movement.Accel:
            vel = Vector(0, 0)
        for inter in self.bots:
            impulse = -FORCE_SENSITIVITY * delta_time * potential.gradient(inter.pos, bot.pos)
            delta_v = impulse
            delta_total = delta_total + delta_v
            if vector.length(delta_v) > vector.length(delta_max):
                delta_max = delta_v
            vel = Vector(vel.x + delta_v.x,
                         vel.y + delta_v.y)
            if self.movement_law == Movement.Dir:
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
