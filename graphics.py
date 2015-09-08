import pygame

from vector import Point

GRID_COLOR = 100,100,100
AXES_COLOR = 155,155,155
OBSTACLE_COLOR = 0,140,0
BOT_COLOR = 255,0,0
TARGET_COLOR=255,255,0
SENSOR_COLOR=50,50,155

TARGET_RADIUS = 5

DRAW_COORD_GRID = True
DRAW_SENSING_AREA = True


class Graphics:
    def __init__(self, field, size = (1024, 768)):
        self.field = field
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("potential")


    def draw_coordinate_grid(self, num = (10,10)):
        for x in xrange(int(self.field.left), 1 + int(self.field.right), 1):
            pygame.draw.line(self.screen, GRID_COLOR if x != 0 else AXES_COLOR,
                             self.field.fit_on_screen(Point(x, self.field.bottom)),
                             self.field.fit_on_screen(Point(x, self.field.top)))
        for y in xrange(int(self.field.bottom), 1 + int(self.field.top), 1):
            pygame.draw.line(self.screen, GRID_COLOR if y != 0 else AXES_COLOR,
                             self.field.fit_on_screen(Point(self.field.left,  y)),
                             self.field.fit_on_screen(Point(self.field.right, y)))


    def render(self, bots, obstacles = [], targets = []):
        self.screen.fill((0, 0, 0))

        if DRAW_COORD_GRID:
            self.draw_coordinate_grid()

        for obstacle in obstacles:
            obstacle.draw(self.screen, self.field)

        for target in targets:
            pygame.draw.circle(self.screen, TARGET_COLOR,
                               self.field.fit_on_screen(target),
                               TARGET_RADIUS, 1)
        
        if DRAW_SENSING_AREA:
            for bot in bots:
                pygame.draw.circle(self.screen, SENSOR_COLOR,
                                   self.field.fit_on_screen(bot.real.pos),
                                   self.field.scale(bot.virtual.obstacle_sensing_distance),
                                   1)
        for bot in bots:
            pygame.draw.circle(self.screen, BOT_COLOR,
                               self.field.fit_on_screen(bot.real.pos),
                               self.field.scale(bot.virtual.radius), 1)