from vector import Point
import obstacle

maps = [[] for i in xrange(10)]

maps[0] = list(obstacle.polygon_to_obstacles([Point(0.0, -3.0),
                                              Point(3.0, -3.0),
                                              Point(3.0,  3.0),
                                              Point(0.0,  3.0),
                                              Point(0.0,  2.0),
                                              Point(2.0,  2.0),
                                              Point(2.0, -2.0),
                                              Point(0.0, -2.0)]))

maps[1] = [obstacle.create_obstacle_circle(Point(1.25, 0.5), 1.1),
           obstacle.create_obstacle_circle(Point(-1.25, 0.0), 0.2)]

maps[2] = [obstacle.create_obstacle_circle(Point(2 * x, 2 * y), 0.2)
           for x in xrange(-2, 3) for y in xrange(-2, 3)]
