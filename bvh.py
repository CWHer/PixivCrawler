import math
import random
import time


def sqr(x):
    return x * x


# norm=2 dist
#   between box and pos
def dist(a, b):
    d2 = 0
    for i in range(3):
        l = a.mn.pos[i]
        r = a.mx.pos[i]
        if l <= b.pos[i] and b.pos[i] <= r: continue
        d2 += min(sqr(l - b.pos[i]), sqr(r - b.pos[i]))
    return math.sqrt(d2)


class Pos():
    def __init__(self, x, y, z):
        self.pos = [x, y, z]

    def x(self):
        return self.pos[0]

    def y(self):
        return self.pos[1]

    def z(self):
        return self.pos[2]


class Box():
    # mn=mx at leaf node
    def __init__(self, mn, mx):
        self.mn = mn
        self.mx = mx


# bounding_box of 2 Box
def bounding_box(a, b):
    mn = Pos(min(a.mn.x(), b.mn.x()), min(a.mn.y(), b.mn.y()),
             min(a.mn.z(), b.mn.z()))
    mx = Pos(max(a.mx.x(), b.mx.x()), max(a.mx.y(), b.mx.y()),
             max(a.mx.z(), b.mx.z()))
    return Box(mn, mx)


class BVHnode():
    def __init__(self):
        self.box = None
        self.ch = []
        self.fa = None
        self.used_times = 0


class BVH():
    def __init__(self):
        random.seed(time.time())
        self.nodes = []
        self.cnt = 0
        self.dist = None
        self.ans = None

    # list of box
    def build(self, fa, boxes):
        num = len(boxes)
        self.nodes.append(BVHnode())
        now_id = self.cnt
        self.cnt += 1
        self.nodes[now_id].fa = fa
        if not fa == None: self.nodes[fa].ch.append(now_id)
        if num == 1:
            self.nodes[now_id].box = Box(boxes[0], boxes[0])
            return
        if num == 2:
            self.build(now_id, boxes[0:1])
            self.build(now_id, boxes[-1:num])
            ls = self.nodes[now_id].ch[0]
            rs = self.nodes[now_id].ch[1]
            self.nodes[now_id].box = bounding_box(self.nodes[ls].box,
                                                  self.nodes[rs].box)
            return
        axis = random.randint(0, 2)
        boxes.sort(key=lambda x: x.pos[axis])
        mid = num // 2
        self.build(now_id, boxes[0:mid])
        self.build(now_id, boxes[mid:num])
        ls = self.nodes[now_id].ch[0]
        rs = self.nodes[now_id].ch[1]
        self.nodes[now_id].box = bounding_box(self.nodes[ls].box,
                                              self.nodes[rs].box)

    # find closest of Pos q
    #   store ans in self.ans
    def query(self, o, q):
        if len(self.nodes[o].ch) == 0:
            # if self.nodes[o].used_times >= self.REPEAT_TIMES:
            #     # self.nodes[fa]
            #     return
            dis = dist(self.nodes[o].box, q)
            if dis < self.dist:
                self.dist = dis
                self.ans = o
            return

        ls = self.nodes[o].ch[0]
        rs = self.nodes[o].ch[1]
        ld = dist(self.nodes[ls].box, q)
        # avoid searching same node
        rd = (1 << 30) if ls == rs else dist(self.nodes[rs].box, q)
        if ld <= rd:
            if ld < self.dist: self.query(ls, q)
            if rd < self.dist: self.query(rs, q)
        else:
            if rd < self.dist: self.query(rs, q)
            if ld < self.dist: self.query(ls, q)

    # f=1 remove/ f=0 modify
    def remove(self, o, f):
        fa = self.nodes[o].fa
        if fa == None: return
        if f == 0:
            ls = self.nodes[fa].ch[0]
            rs = self.nodes[fa].ch[1]
            self.nodes[fa].box = bounding_box(self.nodes[ls].box,
                                              self.nodes[rs].box)
            self.remove(fa, 0)
            return
        # f==1
        if self.nodes[fa].ch[0] != self.nodes[fa].ch[1]:
            k = self.nodes[fa].ch[1] == o
            self.nodes[fa].ch[k] = self.nodes[fa].ch[k ^ 1]
            self.nodes[fa].box = self.nodes[self.nodes[fa].ch[k]].box
            self.remove(fa, 0)
        else:
            self.remove(fa, 1)


# # debug begin
# group = [
#     Pos(random.random(), random.random(), random.random()) for i in range(100)
# ]
# t = BVH(0)
# t.build(None, group)
# print(t.nodes[0].box.mn.pos)
# t.dist = 10000
# ask = Pos(random.random(), random.random(), random.random())
# t.query(0, ask)
# print(t.dist)
# ans = t.nodes[t.ans].box.mx
# print("({}, {}, {})".format(ans.pos[0], ans.pos[1], ans.pos[2]))
# t.remove(t.ans, 1)
# t.dist = 10000
# t.query(0, ask)
# print(t.dist)
# ans = t.nodes[t.ans].box.mx
# print("({}, {}, {})".format(ans.pos[0], ans.pos[1], ans.pos[2]))
# d = 10000
# for dot in group:
#     d = min(dist(Box(dot, dot), ask), d)
# print(d)
# # debug end
