import pygame

from vector import Point

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
WHITE = 255, 255, 255

GRID_COLOR = 100,100,100
AXES_COLOR = 155,155,155

TARGET_RADIUS = 5

DRAW_COORD_GRID = True
DRAW_FORCE_FIELD = False


class Graphics:
    def __init__(self, field, size = (1024, 768)):
        self.field = field
        self.size = size
        self.screen = pygame.display.set_mode(size)


    def draw_coordinate_grid(self, num = (10,10)):
        for x in xrange(int(self.field.left), int(self.field.right), 1):
            pygame.draw.line(self.screen, GRID_COLOR if x != 0 else AXES_COLOR,
                             self.field.fit_on_screen(Point(x, self.field.bottom)),
                             self.field.fit_on_screen(Point(x, self.field.top)))
        for y in frange(int(self.field.bottom), int(self.field.top), 1):
            pygame.draw.line(self.screen, GRID_COLOR if y != 0 else AXES_COLOR,
                             self.field.fit_on_screen(Point(self.field.left,  y)),
                             self.field.fit_on_screen(Point(self.field.right, y)))


    def draw_force_field(self):
        for bx in xrange(-10, 10):
            for by in xrange(-10, 10):
                x = bx / 10.0
                y = by / 10.0
                a = Point(x, y)
                b = a
                force = Vector(0, 0)
                for inter in self.interactors:
                    if (inter is not self):
                        try:
                            d_force = inter.interact(a)
                            force = Vector(force.x + d_force.x, force.y + d_force.y)
                        except: pass
                try:
                    force = vector.normalize(force)
                except: pass
                b = Point(b.x + 0.1 * force.x, b.y + 0.1 * force.y)
                pygame.draw.line(self.screen, (0, 0, 255),
                                 self.field.fit_on_screen(a),
                                 self.field.fit_on_screen(b))


    def render(self, bots, targets = None):
        self.screen.fill((0, 0, 0))

        if DRAW_COORD_GRID:
            self.draw_coordinate_grid()
        if DRAW_FORCE_FIELD:
            self.draw_force_field()

        if targets is not None:
            for target in targets:
                pygame.draw.circle(self.screen, YELLOW,
                                   self.field.fit_on_screen(target, self.size),
                                   TARGET_RADIUS, 1)
        for obj in bots:
            pygame.draw.circle(self.screen, RED,
                               self.field.fit_on_screen(obj.pos),
                               self.field.scale(obj.radius), 1)
        pygame.display.flip()
