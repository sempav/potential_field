from base import BehaviorBase
from bot import BOT_RADIUS, \
                MAX_SENSING_DISTANCE, KNOW_BOT_POSITIONS, \
                OBSTACLE_CLEARANCE, BOT_VEL_CAP
from engine import Movement
import potential
from sensor import Sensor
from vector import Vector, length, normalize, dist
from math import pi, atan2
import graphics


_FORCE_SENSITIVITY = 5e-4


class SensorBased(BehaviorBase):
    def __init__(self, movement=Movement.Accel, 
                 max_sensing_distance = MAX_SENSING_DISTANCE,
                 num_sensors=32,
                 sensor_angles=None):
        self.movement = movement
        self.radius = BOT_RADIUS
        self.max_sensing_distance = max_sensing_distance
        if sensor_angles is None:
            sensor_angles = [(x * 2 * pi) / num_sensors for x in xrange(num_sensors)]
        self.sensors = [Sensor(ang, self.radius, max_sensing_distance)
                        for ang in sensor_angles]


    def calc_desired_velocity(self, bots, obstacles, targets):
        vel = self.vel
        if self.movement != Movement.Accel:
            vel = Vector(0, 0)
        for inter in bots:
            if (not KNOW_BOT_POSITIONS) and dist(inter.real.pos, self.pos) > self.max_sensing_distance:
                continue
            force = -potential.gradient(potential.morse(r0=2 * BOT_RADIUS, k=2.5, a=4.0),
                                        dist(inter.real.pos, self.pos),
                                        self.pos - inter.real.pos,
                                        self.radius + inter.virtual.radius)
            vel += _FORCE_SENSITIVITY * force

        for target in targets:
            force = -potential.gradient(potential.linear(k=-2.0),
                                        dist(target, self.pos),
                                        target - self.pos,
                                        0)
            vel += _FORCE_SENSITIVITY * force

        #ang = atan2(self.vel.y, self.vel.x)
        ang = 0
        self.distances = []
        for s in self.sensors:
            d = s.get_distance(self.pos, ang, obstacles)
            self.distances.append(d)
            if d < self.max_sensing_distance:
                force = -potential.gradient(potential.inverse_quadratic(k=0.5),
                                            d,
                                            -s.get_ray(self.pos, ang).dir,
                                            0 * OBSTACLE_CLEARANCE + self.radius)
                vel += _FORCE_SENSITIVITY * force

        if self.movement == Movement.Dir:
            if length(vel) > 0:
                vel = normalize(vel)
        return vel


    def draw(self, screen, field):
        for s, d in zip(self.sensors, self.distances):
            r = s.get_ray(self.pos, 0 * atan2(self.vel.y, self.vel.x))
            graphics.draw_line(screen, field, (115, 115, 200),
                               r.orig,
                               r.orig + r.dir * d,
                               1)
