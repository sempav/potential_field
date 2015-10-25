from base import BehaviorBase
from engine.bot import BOT_RADIUS, \
                MAX_SENSING_DISTANCE, KNOW_BOT_POSITIONS, \
                OBSTACLE_CLEARANCE, BOT_VEL_CAP, BOT_ACCEL_CAP
from engine import Movement
import potential
from sensor import Sensor
from engine.vector import Vector, length, normalize, dist, signed_angle
from math import pi, atan2, cos, degrees
from engine import graphics


_FORCE_SENSITIVITY = 1.0
COLLISION_CHECK = True
CRITICAL_DIST = 0.5 * BOT_RADIUS
CRITICAL_VEL = 1e-6
COLLISION_DELTA_TIME = BOT_VEL_CAP / BOT_ACCEL_CAP
ROTATE_SENSORS = True


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
        self.obstacle_force_coeff = 1.0 / num_sensors


    def get_heading_angle(self):
        return atan2(-self.real_dir.x, self.real_dir.y)


    def calc_desired_velocity(self, bots, obstacles, targets):
        vel = self.real_vel
        self.collision_delta_time = length(vel) / BOT_ACCEL_CAP
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
            force = -potential.gradient(potential.linear(k=-10.0),
                                        dist(target, self.pos),
                                        target - self.pos,
                                        0)
            vel += _FORCE_SENSITIVITY * force


        if ROTATE_SENSORS:
            ang = self.get_heading_angle()
        else:
            ang = 0.0
        self.distances = []
        for s in self.sensors:
            d = s.get_distance(self.pos, ang, obstacles)
            self.distances.append(d)
            if d < self.max_sensing_distance:
                force = -potential.gradient(potential.inverse_quadratic(k=1.5),
                                            d,
                                            -s.get_ray(self.pos, ang).dir,
                                            OBSTACLE_CLEARANCE)
                vel += _FORCE_SENSITIVITY * force * self.obstacle_force_coeff

        if self.movement == Movement.Dir:
            if length(vel) > 0:
                vel = normalize(vel)

        # TODO: get max_vel from corresponding Model
        if length(vel) > BOT_VEL_CAP:
            vel = normalize(vel) * BOT_VEL_CAP

        self.virtual_vel_before_check = vel
        if COLLISION_CHECK:
            # check for possible collisions:
            # stop moving forward if an obstacle is nearby
            collision = False
            abs_vel = length(vel)
            if ROTATE_SENSORS:
                ang = self.get_heading_angle()
            else:
                ang = 0.0
            for cur_d, s in zip(self.distances, self.sensors):
                if cur_d == s.max_distance:
                    continue
                r = s.get_ray(self.pos, ang)
                c = cos(signed_angle(vel, r.dir))
                new_d = cur_d - c * abs_vel * self.collision_delta_time
                if new_d < CRITICAL_DIST and new_d < cur_d:
                    collision = True
                    break
            if not collision:
                # separate check for possible collision with another bot
                for inter in bots:
                    # don't count collsions with self
                    if inter.virtual is self:
                        continue
                    new_d = dist(inter.real.pos + self.collision_delta_time * inter.real.vel,
                                 self.pos + self.collision_delta_time * vel)
                    new_d -= (self.radius + inter.real.radius)
                    cur_d = dist(inter.real.pos, self.pos)
                    cur_d -= (self.radius + inter.real.radius)
                    if d <= CRITICAL_DIST and new_d < cur_d:
                        collision = True
                        break
            if collision:
                vel = normalize(vel) * CRITICAL_VEL
                self.collision = True
            else:
                self.collision = False

        return vel


    def draw(self, screen, field):
        if graphics.DRAW_SENSOR_RAYS:
            if ROTATE_SENSORS:
                ang = self.get_heading_angle()
            else:
                ang = 0.0
            for s, d in zip(self.sensors, self.distances):
                r = s.get_ray(self.pos, ang)
                graphics.draw_line(screen, field, (115, 115, 200),
                                   r.orig,
                                   r.orig + r.dir * d,
                                   1)
        if COLLISION_CHECK and self.collision:
            # draw small purple circle indicating collision state
            graphics.draw_circle(screen, field, (255, 0, 255),
                                 self.pos,
                                 0.5 * BOT_RADIUS)
            # draw projections of virtual velocity onto sensor rays
            if graphics.DRAW_SENSOR_RAYS:
                vel_ang = signed_angle(self.virtual_vel_before_check, Vector(0.0, 1.0))
                abs_vel = length(self.virtual_vel_before_check)
                if ROTATE_SENSORS:
                    ang = self.get_heading_angle()
                else:
                    ang = 0.0
                for s in self.sensors:
                    r = s.get_ray(self.pos, ang)
                    c = cos(signed_angle(self.virtual_vel_before_check, r.dir))
                    proj = c * abs_vel;
                    if proj < 0:
                        continue
                    graphics.draw_line(screen, field, (115, 200, 200),
                                       r.orig,
                                       r.orig + r.dir * proj,
                                       2)
            v = Vector(0.0, 0.0)
            try:
                v = 0.5 * normalize(self.virtual_vel_before_check)
            except ZeroDivisionError:
                pass
            # draw virtual velocity vector that was picked before collision check
            graphics.draw_line(screen, field, (0, 200, 0),
                               self.pos,
                               self.pos + v,
                               1)
