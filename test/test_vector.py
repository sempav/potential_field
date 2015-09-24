import unittest
import vector
from vector import Vector, Point, geom_places, length, dist
from vector import normalize, dot, cross, angle, signed_angle
from vector import rotate

class VectorTestCase(unittest.TestCase):
    def testLength(self):
        self.assertAlmostEqual(length(Vector(0.0, 0.0)), 0.0, geom_places)
        self.assertAlmostEqual(length(Vector(1.0, 1.0)), 2**0.5, geom_places)

        v = normalize(Vector(0.23, 1.45))
        self.assertAlmostEqual(length(v * 23.145), 23.145)
        self.assertAlmostEqual(length(v / 23.145), 1.0/23.145)


    def testDist(self):
        self.assertAlmostEqual(dist(Point(0.0, 0.0), Point(0.0, 0.0)),
                               0.0, geom_places)
        self.assertAlmostEqual(dist(Point(1.0, 2.0), Point(0.0, 3.0)),
                               2**0.5, geom_places)


    def testNormalize(self):
        self.assertEqual(normalize(Vector(2.0, 2.0)),
                         Vector(0.5 * 2**0.5, 0.5 * 2**0.5))
        self.assertEqual(normalize(Vector(0.01, 0.0)),
                         Vector(1.0, 0.0))
        with self.assertRaises(ZeroDivisionError):
            normalize(Vector(0.0, 0.0))


    def testDotProduct(self):
        self.assertAlmostEqual(dot(Vector(1.0, 0.0), Vector(0.0, 1.0)),
                               0.0, geom_places)
        self.assertAlmostEqual(dot(Vector(1.0, 1.0), Vector(-1.0, 1.0)),
                               0.0, geom_places)
        self.assertAlmostEqual(dot(Vector(2.0, 0.0), Vector(2.0, 0.0)),
                               4.0, geom_places)
        self.assertAlmostEqual(dot(Vector(1.0, 2.0), Vector(-1.0, 4.0)),
                               7.0, geom_places)


    def testCrossProduct(self):
        self.assertAlmostEqual(cross(Vector(1.0, 0.0), Vector(0.0, 1.0)),
                               1.0, geom_places)
        self.assertAlmostEqual(cross(Vector(0.0, 1.0), Vector(1.0, 0.0)),
                               -1.0, geom_places)


    def testAngle(self):
        from math import pi
        self.assertAlmostEqual(signed_angle(Vector(1.0, 0.0), Vector(0.0, 1.0)),
                               pi / 2)
        self.assertAlmostEqual(angle(Vector(1.0, 0.0), Vector(0.0, 1.0)),
                               pi / 2)

        self.assertAlmostEqual(signed_angle(Vector(-1.0, 1.0), Vector(1.0, 1.0)),
                               -pi / 2)
        self.assertAlmostEqual(angle(Vector(-1.0, 1.0), Vector(1.0, 1.0)),
                               pi / 2)

        self.assertAlmostEqual(signed_angle(Vector(1.0, 0.0), Vector(100.0, 100.0)),
                               pi / 4)
        self.assertAlmostEqual(angle(Vector(1.0, 0.0), Vector(100.0, 100.0)),
                               pi / 4)

        self.assertAlmostEqual(abs(signed_angle(Vector(-100.0, 0.0), Vector(0.01, 0.0))),
                               pi)
        self.assertAlmostEqual(angle(Vector(-100.0, 0.0), Vector(0.01, 0.0)),
                               pi)


    def testRotate(self):
        from math import pi
        self.assertEqual(rotate(Vector(2.0, 0.0), pi/4), Vector(2**0.5, 2**0.5))
        self.assertEqual(rotate(Vector(0.0, 100.0), pi), Vector(0.0, -100.0))
        self.assertEqual(rotate(Vector(1.46, 1.75), -2 * pi), Vector(1.46, 1.75))
