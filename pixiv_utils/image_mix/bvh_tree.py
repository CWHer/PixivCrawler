from __future__ import annotations

import dataclasses
import math
import random
from collections import namedtuple
from typing import List, Optional

from utils import assertError

Point = namedtuple("Point", ["x", "y", "z"])


class Box:
    def __init__(self, min_p: Point, max_p: Point):
        # NOTE: max_p == min_p at leaf node
        self.min_p = min_p
        self.max_p = max_p

    @staticmethod
    def boundingBox(a: Box, b: Box) -> Box:
        min_p = Point(
            min(a.min_p.x, b.min_p.x), min(a.min_p.y, b.min_p.y), min(a.min_p.z, b.min_p.z)
        )
        max_p = Point(
            max(a.max_p.x, b.max_p.x), max(a.max_p.y, b.max_p.y), max(a.max_p.z, b.max_p.z)
        )
        return Box(min_p, max_p)

    def dist(self, point: Point) -> float:
        """[summary]
        Norm = 2 dist, between box and pos
        """
        d2 = 0
        for i in range(3):
            low = self.min_p[i]
            high = self.max_p[i]
            if low <= point[i] and point[i] <= high:
                continue
            d2 += (low - point[i]) ** 2 if point[i] <= low else (high - point[i]) ** 2
        return math.sqrt(d2)


@dataclasses.dataclass
class BVHNode:
    father: Optional[BVHNode] = None
    used_times: int = 0
    box: Optional[Box] = None
    child: List[BVHNode] = dataclasses.field(default_factory=list)


class BVHTree:
    def __init__(self, MAX_TIMES: int):
        self.root: Optional[BVHNode] = None
        self.nodes: List[BVHNode] = []
        self.MAX_TIMES = MAX_TIMES
        self.reset()

    def reset(self):
        # NOTE: reset query answer
        self.min_dist: float = float("inf")
        self.closest_node: Optional[BVHNode] = None

    def build(self, father: Optional[BVHNode], points: List[Point]) -> None:
        num_points = len(points)
        current = BVHNode(father=father)
        self.nodes.append(current)
        if father is not None:
            father.child.append(current)
        else:
            self.root = current

        if num_points == 1:
            current.box = Box(points[0], points[0])
            return
        if num_points == 2:
            self.build(current, [points[0]])
            self.build(current, [points[-1]])
            current.box = Box.boundingBox(current.child[0].box, current.child[1].box)
            return

        axis = random.randint(0, 2)
        points.sort(key=lambda x: x[axis])
        mid = num_points // 2
        self.build(current, points[0:mid])
        self.build(current, points[mid:num_points])
        current.box = Box.boundingBox(current.child[0].box, current.child[1].box)

    def query(self, q: Point, x: Optional[BVHNode] = None) -> None:
        """[summary]
        Find the point in the tree, that is closest to a given q
        """
        if x is None:
            x: BVHNode = self.root

        if len(x.child) == 0:
            if x.used_times >= self.MAX_TIMES:
                return
            dist = x.box.dist(q)
            if dist < self.min_dist:
                self.min_dist = dist
                self.closest_node = x
            return

        children = [(x.child[i], x.child[i].box.dist(q)) for i in range(2)]
        children.sort(key=lambda x: x[-1])
        for child, dist in children:
            if dist < self.min_dist:
                self.query(q, child)

    def remove(self, x: BVHNode):
        """[summary]
        NOTE: x must be a leaf node
        """
        # NOTE: replace x.father with x.brother
        y: BVHNode = x.father
        assertError(y is not None, "BVH tree is empty, please increase MAX_TIMES")
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
            current.box = Box.boundingBox(current.child[0].box, current.child[1].box)
            current = current.father
