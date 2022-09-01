from __future__ import annotations

import math
import random
from typing import List, Optional

from utils import printError


class Point():
    def __init__(self, x, y, z):
        self.pos = [x, y, z]

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def z(self):
        return self.pos[2]


class Box():
    def __init__(self, min_p: Point, max_p: Point):
        # NOTE: max_p == min_p at leaf node
        self.min_p = min_p
        self.max_p = max_p

    @staticmethod
    def boundingBox(a: Box, b: Box) -> Box:
        min_p = Point(min(a.min_p.x, b.min_p.x),
                      min(a.min_p.y, b.min_p.y),
                      min(a.min_p.z, b.min_p.z))
        max_p = Point(max(a.max_p.x, b.max_p.x),
                      max(a.max_p.y, b.max_p.y),
                      max(a.max_p.z, b.max_p.z))
        return Box(min_p, max_p)

    def dist(self, point: Point) -> float:
        """[summary]
        norm = 2 dist, between box and pos
        """
        d2 = 0
        for i in range(3):
            low = self.min_p.pos[i]
            high = self.max_p.pos[i]
            if low <= point.pos[i] \
                    and point.pos[i] <= high:
                continue
            d2 += (low - point.pos[i]) ** 2 \
                if point.pos[i] <= low else (high - point.pos[i]) ** 2
        return math.sqrt(d2)


class BVHNode():
    def __init__(self, father):
        self.used_times = 0
        self.father = father
        self.box: Optional[Box] = None
        self.child: List[BVHNode] = []


class BVH():
    def __init__(self, MAX_TIMES: int):
        random.seed(0)
        self.root: Optional[BVHNode] = None
        self.nodes: List[BVHNode] = []
        self.MAX_TIMES = MAX_TIMES
        self.reset()

    def reset(self):
        # NOTE: query answer
        self.dist: float = float("inf")
        self.ans: Optional[BVHNode] = None

    def build(self,
              father: Optional[BVHNode],
              points: List[Point]) -> None:
        n_box = len(points)
        current = BVHNode(father)
        self.nodes.append(current)
        if father is not None:
            father.child.append(current)
        else:
            self.root = current

        if n_box == 1:
            current.box = Box(points[0], points[0])
            return
        if n_box == 2:
            self.build(current, [points[0]])
            self.build(current, [points[-1]])
            current.box = Box.boundingBox(
                current.child[0].box, current.child[1].box)
            return

        axis = random.randint(0, 2)
        points.sort(key=lambda x: x.pos[axis])
        mid = n_box // 2
        self.build(current, points[0:mid])
        self.build(current, points[mid:n_box])
        current.box = Box.boundingBox(
            current.child[0].box, current.child[1].box)

    def query(self, q: Point,
              x: Optional[BVHNode] = None) -> None:
        """[summary]
        find the point in the tree, that is closest to a given q
        """
        if x is None:
            x: BVHNode = self.root

        if len(x.child) == 0:
            if x.used_times >= \
                    self.MAX_TIMES:
                return
            dist = x.box.dist(q)
            if dist < self.dist:
                self.dist = dist
                self.ans = x
            return

        children = [
            (x.child[i], x.child[i].box.dist(q))
            for i in range(2)]
        children.sort(key=lambda x: x[-1])
        for child, dist in children:
            if dist < self.dist:
                self.query(q, child)

    def remove(self, x: BVHNode):
        """[summary]
        x must be a leaf node
        """
        # NOTE: replace x.father with x.brother
        y: BVHNode = x.father
        printError(
            y is None, "BVH tree is empty, "
            "please increase MAX_TIMES")
        z: BVHNode = y.father
        t = y.child[y.child[0] == x]
        t.father = z
        if z is not None:
            k = z.child[1] == y
            z.child[k] = t
        else:
            self.root = t

        current = z
        while current is not None:
            current.box = Box.boundingBox(
                current.child[0].box, current.child[1].box)
            current = current.father


if __name__ == "__main__":
    # debug
    def genPoint():
        return Point(random.random(),
                     random.random(),
                     random.random())

    bvh_tree = BVH(MAX_TIMES=1)
    points = [genPoint() for _ in range(100)]
    bvh_tree.build(father=None, points=points)
    print(bvh_tree.root.box.min_p.pos, bvh_tree.root.box.max_p.pos)

    q = genPoint()
    bvh_tree.query(q)
    print(bvh_tree.dist)
    ans = bvh_tree.ans.box.max_p
    print(f"({ans.x}, {ans.y}, {ans.z})")
    bvh_tree.remove(bvh_tree.ans)
    # t.ans.used_times += 1

    bvh_tree.reset()
    bvh_tree.query(q)
    print(bvh_tree.dist)
    ans = bvh_tree.ans.box.max_p
    print(f"({ans.x}, {ans.y}, {ans.z})")

    distances = [
        Box(point, point).dist(q) for point in points]
    distances.sort()
    print(distances[:5])
