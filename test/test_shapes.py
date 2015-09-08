import unittest
from vector import Point, Vector
from shapes import Ray, Circle, Segment, Polygon


class CircleTestCase(unittest.TestCase):
    def testTwoIntersections(self):
        c = Circle(Point(0.0, 0.0), 1.0)

        p = Ray(Point(-2.0, 0.0), Vector(1.0, 0.0)).intersect(c)
        self.assertEqual(p, Point(-1.0, 0.0))

        c = Circle(Point(0.0, 0.0), 2.0)
        p = Ray(Point(100.0, 100.0), Vector(-1.0, -1.0)).intersect(c)
        self.assertEqual(p, Point(2**0.5, 2**0.5))

        c = Circle(Point(10.0, 10.0), 4.0)
        p = Ray(Point(0.0, 0.0), Vector(1.0, 1.0)).intersect(c)
        self.assertEqual(p, Point(10.0 - 2 * 2**0.5, 10.0 - 2 * 2**0.5))


    def testOneIntersectionWithOrigInsideCircle(self):
        c = Circle(Point(0.0, 0.0), 1.0)

        p = Ray(Point(0.0, 0.0), Vector(1.0, 0.0)).intersect(c)
        self.assertEqual(p, Point(1.0, 0.0))

        p = Ray(Point(0.0, 0.0), Vector(1.0, 1.0)).intersect(c)
        self.assertEqual(p, Point(0.5 * 2**0.5, 0.5 * 2**0.5))


    def testOneIntersectionWithIncidentRay(self):
        c = Circle(Point(0.0, 0.0), 1.0)

        p = Ray(Point(-10.0, 1.0), Vector(1.0, 0.0)).intersect(c)
        self.assertEqual(p, Point(0.0, 1.0))
        
        p = Ray(Point(-10.0 - 0.5 * 2**0.5, -10.0 + 0.5 * 2**0.5), Vector(1.0, 1.0)).intersect(c)
        self.assertEqual(p, Point(-0.5 * 2**0.5, 0.5 * 2**0.5))


    def testNoIntersection(self):
        c = Circle(Point(10.0, 10.0), 1.0)

        p = Ray(Point(0.0, 0.0), Vector(1.0, 0.0)).intersect(c)
        self.assertIsNone(p)

        p = Ray(Point(0.0, 0.0), Vector(-1.0, -1.0)).intersect(c)
        self.assertIsNone(p)


class SegmentTestCase(unittest.TestCase):
    def testMiddleIntersection(self):
        s = Segment(Point(-1.0, 0.0), Point(1.0, 0.0))

        p = Ray(Point(-1.0, -1.0), Vector(1.0, 1.0)).intersect(s)
        self.assertEqual(p, Point(0.0, 0.0))

        p = Ray(Point(-2.0, -1.0), Vector(2.75, 1.0)).intersect(s)
        self.assertEqual(p, Point(0.75, 0.0))


    def testBoundsIntersection(self):
        s = Segment(Point(-1.0, 0.0), Point(1.0, 0.0))

        p = Ray(Point(-1.0, -1.0), Vector(0.0, 1.0)).intersect(s)
        self.assertEqual(p, Point(-1.0, 0.0))

        p = Ray(Point(-2.0, -2.0), Vector(3.0, 2.0)).intersect(s)
        self.assertEqual(p, Point(1.0, 0.0))

    def testNoIntersection(self):
        s = Segment(Point(-1.0, 0.0), Point(1.0, 0.0))

        p = Ray(Point(-1.0, -1.0), Vector(1.0, 0.0)).intersect(s)
        self.assertIsNone(p)

        p = Ray(Point(0.5, 1.0), Vector(1.0, 1.0)).intersect(s)
        self.assertIsNone(p)

        p = Ray(Point(0.0, 1.0), Vector(0.0, 1.0)).intersect(s)
        self.assertIsNone(p)

        s = Segment(Point(-1.0, -1.0), Point(1.0, -1.0))
        p = Ray(Point(0.0, 0.0), Vector(1.0, 1.0)).intersect(s)
        self.assertIsNone(p)

        s = Segment(Point(-1.0, 1.0), Point(-1.0, -1.0))
        p = Ray(Point(0.0, 0.0), Vector(1.0, 1.0)).intersect(s)
        self.assertIsNone(p)


class PolygonTestCase(unittest.TestCase):
    def testOneIntersection(self):
        s = Polygon([Point(-1.0, -1.0), Point(1.0, -1.0),
                     Point(1.0, 1.0),   Point(-1.0, 1.0)])

        p = Ray(Point(0.0, 0.0), Vector(1.0, 0.0)).intersect(s)
        self.assertEqual(p, Point(1.0, 0.0))

        p = Ray(Point(0.0, 0.0), Vector(1.0, 1.0)).intersect(s)
        self.assertEqual(p, Point(1.0, 1.0))


    def testMultipleIntersections(self):
        s = Polygon([Point(-1.0, -1.0), Point(1.0, -1.0),
                     Point(1.0, 1.0),   Point(-1.0, 1.0)])

        p = Ray(Point(-2.0, 0.0), Vector(1.0, 0.5)).intersect(s)
        self.assertEqual(p, Point(-1.0, 0.5))

        p = Ray(Point(-5.0, -2.0), Vector(4.0, 1.0)).intersect(s)
        self.assertEqual(p, Point(-1.0, -1.0))

        p = Ray(Point(-3.0, 0.0), Vector(4.0, 1.0)).intersect(s)
        self.assertEqual(p, Point(-1.0, 0.5))


    def testNoIntersection(self):
        s = Polygon([Point(-1.0, -1.0), Point(1.0, -1.0),
                     Point(1.0, 1.0),   Point(-1.0, 1.0)])

        p = Ray(Point(-2.0, 0.0), Vector(1.0, 2.0)).intersect(s)
        self.assertIsNone(p)

        p = Ray(Point(2.0, 0.0), Vector(1.0, 0.0)).intersect(s)
        self.assertIsNone(p)

        p = Ray(Point(2.0, 2.0), Vector(1.0, 1.0)).intersect(s)
        self.assertIsNone(p)

        p = Ray(Point(2.0, 0.5), Vector(1.0, 0.1)).intersect(s)
        self.assertIsNone(p)
