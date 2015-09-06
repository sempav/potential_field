import unittest
import vector
from vector import Vector, Point, geom_places

class VectorTestCase(unittest.TestCase):
    def testLength(self):
        self.assertAlmostEqual(vector.length(Vector(0.0, 0.0)), 0.0, geom_places)
        self.assertAlmostEqual(vector.length(Vector(1.0, 1.0)), 2**0.5, geom_places)


    def testDist(self):
        self.assertAlmostEqual(vector.dist(Point(0.0, 0.0), Point(0.0, 0.0)),
                               0.0, geom_places)
        self.assertAlmostEqual(vector.dist(Point(1.0, 2.0), Point(0.0, 3.0)),
                               2**0.5, geom_places)


    def testNormalize(self):
        self.assertEqual(vector.normalize(Vector(2.0, 2.0)),
                         Vector(0.5 * 2**0.5, 0.5 * 2**0.5))
        self.assertEqual(vector.normalize(Vector(0.01, 0.0)),
                         Vector(1.0, 0.0))
        with self.assertRaises(ZeroDivisionError):
            vector.normalize(Vector(0.0, 0.0))


    def testDotProduct(self):
        self.assertAlmostEqual(vector.dot(Vector(1.0, 0.0), Vector(0.0, 1.0)),
                               0.0, geom_places)
        self.assertAlmostEqual(vector.dot(Vector(1.0, 1.0), Vector(-1.0, 1.0)),
                               0.0, geom_places)
        self.assertAlmostEqual(vector.dot(Vector(2.0, 0.0), Vector(2.0, 0.0)),
                               4.0, geom_places)
        self.assertAlmostEqual(vector.dot(Vector(1.0, 2.0), Vector(-1.0, 4.0)),
                               7.0, geom_places)


    def testCrossProduct(self):
        self.assertAlmostEqual(vector.cross(Vector(1.0, 0.0), Vector(0.0, 1.0)),
                               1.0, geom_places)
        self.assertAlmostEqual(vector.cross(Vector(0.0, 1.0), Vector(1.0, 0.0)),
                               -1.0, geom_places)
        #self.assertAlmostEqual(
