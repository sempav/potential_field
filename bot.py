from vector import Vector, Point, dist, length, normalize
from engine import Movement


BOT_RADIUS = 0.3
BOT_ACCEL_CAP = 10.0
BOT_VEL_CAP = 1.0

MAX_SENSING_DISTANCE = 5 * BOT_RADIUS
OBSTACLE_CLEARANCE = 0.0 * BOT_RADIUS
KNOW_BOT_POSITIONS = True


class Bot():
    def __init__(self, model, behavior):
        self.virtual = behavior
        self.real = model
        self.virtual.sync_to_real(self.real)

    def draw(self, screen, field):
        self.real.draw(screen, field)
        self.virtual.draw(screen, field)
