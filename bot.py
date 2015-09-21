from vector import Vector, Point, dist, length, normalize
from engine import Movement


BOT_RADIUS = 0.3
BOT_ACCEL_CAP = 1e-5
BOT_VEL_CAP = 2e-3

MAX_SENSING_DISTANCE = 5 * BOT_RADIUS
OBSTACLE_CLEARANCE = 0.5 * BOT_RADIUS
KNOW_BOT_POSITIONS = True


class Bot():
    def __init__(self, model, behavior):
        self.virtual = behavior
        self.real = model
        self.virtual.sync_to_real(self.real)
