import sys
sys.path.append('.')
from utils.grid import *
from utils.priority_queue import *
from collections import deque
from pathing_base import *
import unittest

inf = float('inf')

class DStarLite(Pathing):
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.U = PriorityQueue()
        self.km = 0
        self.g = Grid(grid.width, grid.height, inf)
        self.rhs = Grid(grid.width, grid.height, inf)
        self.rhs[goal] = 0
        self.U.update(goal, (self._h(start, goal), 0))

    def _update_vertex(self, u):
        if self.g[u] != self.rhs[u]:
            self.U.update(u, self._calculate_key(u))
        elif u in self.U:
            self.U.remove(u)

    def findpath(self):
        while self.U.peek_priority() < self._calculate_key(self.start) or self.rhs[self.start] > self.g[self.start]:
            u = self.U.peek()
            kold = self.U.peek_priority()
            knew = self._calculate_key(u)
            if kold < knew:
                self.U.update(u, knew)
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                self.U.remove(u)
                for s in self._successors(u):
                    if s != self.goal: self.rhs[s] = min(self.rhs[s], self._c(s, u) + self.g[u])
                    self._update_vertex(s)
            else:
                self.U.update(u, knew)
                gold = self.g[u]
                self.g[u] = inf
                for s in self._successors(u) + [u]:
                    if self.rhs[s] == self._c(s, u) + gold:
                        if s != self.goal: self.rhs[s] = min((self._c(s, sp) + self.g[sp] for sp in self._successors(s)))
                    self._update_vertex(s)

    def update(self, changes):
        considered = set()
        for u in changes.keys():
            for v in self._successors(u):
                if (u, v) in considered: continue
                considered.add((u, v))
                considered.add((v, u))
                if v in changes:
                    cold = min(changes[u], changes[v])
                else:
                    cold = min(changes[u], self.g[v])

                if cold > self._c(u, v):
                    if u != self.goal: self.rhs[u] = min(self.rhs[u], self._c(u, v) + self.g[v])
                elif self.rhs[u] == cold + self.g[v]:
                    if u != self.goal: self.rhs[u] = min((self._c(u, s) + self.g[s] for s in self._successors(u)))
                if cold > self._c(u, v):
                    if v != self.goal: self.rhs[v] = min(self.rhs[v], self._c(u, v) + self.g[u])
                elif self.rhs[v] == cold + self.g[u]:
                    if v != self.goal: self.rhs[v] = min((self._c(v, s) + self.g[s] for s in self._successors(v)))

                self._update_vertex(u)
                self._update_vertex(v)
        
        self.findpath()


    def current_move(self):
        return self.start

    def next_move(self):
        moves = [(succ, self._c(self.start, succ) + self.g[succ]) for succ in self._successors(self.start)]
        self.start = min(moves, key=lambda x: x[1])[0]
        return self.start

    def _c(self, s, t):
        """
        Calculates the cost between 2 nodes, s and t.
        s and t must be adjacent in this specific context.
        """
        return max(self.grid[s], self.grid[t])

    def _h(self, s, t):
        """
        Calculates the heuristic between 2 nodes, s and t.
        """
        x1, y1 = s
        x2, y2 = t
        return (abs(x1 - x2) + abs(y1 - y2)) * 10

    def _calculate_key(self, s):
        return (min(self.g[s], self.rhs[s]) + self._h(self.start, s) + self.km,
                min(self.g[s], self.rhs[s]))


class DStarLiteTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10, 10, 10)

    def check_valid_path(self, start, goal, path):
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        prev_x, prev_y = path[0]
        for x, y in path[1:]:
            self.assertEqual(abs(x-prev_x) + abs(y-prev_y), 1)
            prev_x = x
            prev_y = y

    def test_basic(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        path = [pather.current_move()]
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.assertEqual(len(path), 10)
        self.check_valid_path((1, 1), (8, 3), path)

    def test_map_change_simple(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        self.grid[4, 1] = 40
        self.grid[4, 3] = 40
        pather.update({(4, 1): 10, (4, 3): 10})
        path = [pather.current_move()]
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.assertEqual(len(path), 10)
        self.assertIn((4, 2), path)
        self.check_valid_path((1, 1), (8, 3), path)

    def test_map_change_simple2(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        self.grid[4, 1] = 40
        self.grid[4, 2] = 40
        self.grid[4, 3] = 40
        pather.update({(4, 1): 10, (4, 2): 10, (4, 3): 10})
        path = [pather.current_move()]
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.assertEqual(len(path), 12)
        self.assertTrue((4, 4) in path or (4, 0) in path)
        self.check_valid_path((1, 1), (8, 3), path)

    def test_map_change_in_middle(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        path = [pather.current_move()]
        path.append(pather.next_move())
        path.append(pather.next_move())
        self.grid[4, 1] = 40
        self.grid[4, 2] = 40
        self.grid[4, 3] = 40
        pather.update({(4, 1): 10, (4, 2): 10, (4, 3): 10})
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.assertEqual(len(path), 12)
        self.assertTrue((4, 4) in path or (4, 0) in path)
        self.check_valid_path((1, 1), (8, 3), path)

    def test_map_changes_twice(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        path = [pather.current_move()]
        path.append(pather.next_move())
        path.append(pather.next_move())
        self.grid[7, 1] = 40
        self.grid[7, 2] = 40
        self.grid[7, 3] = 40
        pather.update({(7, 1): 10, (7, 2): 10, (7, 3): 10})
        path.append(pather.next_move())
        path.append(pather.next_move())
        path.append(pather.next_move())
        self.grid[7, 2] == 20
        pather.update({(7, 2): 40})
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.assertEqual(len(path), 10)
        self.check_valid_path((1, 1), (8, 3), path)

    def test_map_changes_not_move_back(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        path = [pather.current_move()]
        for i in xrange(6):
            path.append(pather.next_move())
        location_at_change = pather.current_move()
        self.grid[8, 2] = 50
        self.grid[8, 1] = 50
        self.grid[8, 0] = 50
        self.grid[7, 3] = 50
        self.grid[6, 3] = 50
        self.grid[5, 3] = 50
        self.grid[4, 3] = 50
        self.grid[3, 3] = 50
        pather.update({(8, 2): 10, (8, 1): 10, (8, 0): 10, (7, 3): 10, (6, 3): 10, (5, 3): 10, (4, 3): 10, (3, 3): 10})
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        if location_at_change[1] < 3:
            self.assertEqual(len(path), 10)
        elif location_at_change[1] == 3:
            self.assertEqual(len(path), 12)
        self.check_valid_path((1, 1), (8, 3), path)

    def test_map_changes_move_back(self):
        pather = DStarLite(self.grid, (1, 1), (8, 3))
        pather.findpath()
        path = [pather.current_move()]
        for i in xrange(6):
            path.append(pather.next_move())
        location_at_change = pather.current_move()
        self.grid[8, 2] = 500
        self.grid[8, 1] = 500
        self.grid[8, 0] = 500
        self.grid[7, 3] = 500
        self.grid[6, 3] = 500
        self.grid[5, 3] = 500
        self.grid[4, 3] = 500
        self.grid[3, 3] = 500
        self.grid[5, 4] = 500
        pather.update({(8, 2): 10, (8, 1): 10, (8, 0): 10, (7, 3): 10, (6, 3): 10, (5, 3): 10, (4, 3): 10, (3, 3): 10, (5, 4): 10})
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.assertEqual(len(path), 22)
        self.check_valid_path((1, 1), (8, 3), path)

