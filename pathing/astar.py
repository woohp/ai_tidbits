import sys
sys.path.append('.')
from utils.grid import *
from utils.priority_queue import *
from collections import deque
from pathing_base import *


class Node(object):
    def __init__(self, x, y, g, h, parent):
        self.x = x
        self.y = y
        self.loc = (x, y)
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

class AStar(Pathing):
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

    def findpath(self):
        history = Grid(self.grid.width, self.grid.height, inf)
        fringe_score = Grid(self.grid.width, self.grid.height, inf)
        fringe = PriorityQueue()
        start_node = Node(self.start[0], self.start[1],
                0, self._h(self.start, self.goal), None)
        fringe.update(start_node, start_node.f)

        while len(fringe) > 0:
            node, f = fringe.pop()
            print node.loc
            
            if history[node.loc] < inf: continue
            if node.loc == self.goal:
                self.path = deque()
                while node != None:
                    self.path.appendleft(node.loc)
                    node = node.parent
                return True

            for suc in self._successors(node.loc):
                x, y = suc
                cost = self._c(node.loc, suc)
                h = self._h(suc, self.goal)
                nd = Node(x, y, cost, h, node)
                if nd.f < fringe_score[nd.loc]:
                    fringe.update(nd, nd.f)
                    fringe_score[nd.loc] = nd.f

        return False


    def current_move(self):
        return self.path[0]

    def next_move(self):
        self.path.popleft()
        return self.current_move()

    def _h(self, s, t):
        """
        Calculates the heuristic between 2 nodes, s and t.
        """
        x1, y1 = s
        x2, y2 = t
        return (abs(x1 - x2) + abs(y1 - y2)) * 10

    def _c(self, s, t):
        return max(self.grid[s], self.grid[t])


class AStarTest(unittest.TestCase):
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
        pather = AStar(self.grid, (1, 1), (8, 3))
        success = pather.findpath()
        self.assertTrue(success)
        path = [pather.current_move()]
        while pather.current_move() != (8, 3):
            path.append(pather.next_move())
        self.check_valid_path((1, 1), (8, 3), path)
        self.assertEqual(len(path), 10)

    def test_simple_wall(self):
        self.grid[5, 3] = 100
        self.grid[5, 4] = 100
        self.grid[5, 5] = 100
        self.grid[5, 6] = 100
        self.grid[5, 7] = 100
        pather = AStar(self.grid, (3, 5), (7, 5))
        success = pather.findpath()
        self.assertTrue(success)
        path = [pather.current_move()]
        while pather.current_move() != (7, 5):
            path.append(pather.next_move())
        self.check_valid_path((3, 5), (7, 5), path)
        self.assertEqual(len(path), 11)

    def test_failure(self):
        self.grid[1, 0] = inf
        self.grid[0, 1] = inf
        self.grid[1, 1] = inf
        pather = AStar(self.grid, (0, 0), (2, 2))
        success = pather.findpath()
        self.assertFalse(success)

