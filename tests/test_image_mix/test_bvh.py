import math
import random
import unittest

from bvh_tree import Box, BVHTree, Point


class BVHTreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        random.seed(131)

    def testBuild(self):
        bvh_tree = BVHTree(MAX_TIMES=1)
        points = [Point(1, 2, 3), Point(4, 5, 6), Point(7, 8, 9)]
        bvh_tree.build(father=None, points=points)
        self.assertEqual(len(bvh_tree.nodes), 5)
        self.assertEqual(bvh_tree.root.box.min_p, Point(1, 2, 3))
        self.assertEqual(bvh_tree.root.box.max_p, Point(7, 8, 9))

    def testQuery(self):
        bvh_tree = BVHTree(MAX_TIMES=1)
        points = [Point(1, 2, 3), Point(4, 5, 6), Point(7, 8, 9)]
        bvh_tree.build(father=None, points=points)
        q = Point(2, 3, 4)
        bvh_tree.query(q)
        self.assertAlmostEqual(bvh_tree.min_dist, math.sqrt(3))
        self.assertEqual(bvh_tree.closest_node.box.min_p, Point(1, 2, 3))
        self.assertEqual(bvh_tree.closest_node.box.max_p, Point(1, 2, 3))

    def testRemove(self):
        bvh_tree = BVHTree(MAX_TIMES=1)
        points = [Point(1, 2, 3), Point(4, 5, 6), Point(7, 8, 9)]
        bvh_tree.build(father=None, points=points)
        q = Point(2, 3, 4)
        bvh_tree.query(q)
        bvh_tree.remove(bvh_tree.closest_node)
        self.assertEqual(len(bvh_tree.nodes), 5)

        bvh_tree.reset()
        bvh_tree.query(q)
        self.assertAlmostEqual(bvh_tree.min_dist, math.sqrt(12))

    def testComplex(self):
        def genPoint():
            return Point(random.random(), random.random(), random.random())

        bvh_tree = BVHTree(MAX_TIMES=1)
        points = [genPoint() for _ in range(100)]
        bvh_tree.build(father=None, points=points)

        q = genPoint()
        distances = [Box(point, point).dist(q) for point in points]
        distances.sort()

        bvh_tree.query(q)
        self.assertAlmostEqual(bvh_tree.min_dist, distances[0])

        bvh_tree.remove(bvh_tree.closest_node)
        bvh_tree.reset()
        bvh_tree.query(q)
        self.assertAlmostEqual(bvh_tree.min_dist, distances[1])

        bvh_tree.closest_node.used_times += 1
        bvh_tree.reset()
        bvh_tree.query(q)
        self.assertAlmostEqual(bvh_tree.min_dist, distances[2])


if __name__ == "__main__":
    unittest.main()
