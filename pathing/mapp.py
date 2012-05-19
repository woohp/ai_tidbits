import sys
sys.path.append('.')
from utils.grid import *
from utils.priority_queue import *
from collections import deque
from pathing_base import *
from astar import Node, AStar
import itertools

class MAPP(Pathing):
    def __init__(self, grid, starts, goals):
        assert len(starts) == len(goals)
        self.grid = grid
        self.starts = starts
        self.goals = goals

    def findpath(self):
        # compute each path individually along with all the alternative paths
        # using a modified version of A*
        individual_paths = []
        alternative_paths = []
        for start, goal in itertools.izip(self.starts, self.goals):
            history = Grid(self.grid.width, self.grid.height, inf)
            fringe_score = Grid(self.grid.width, self.grid.height, inf)
            fringe = PriorityQueue()
            start_node = Node(start[0], start[1],
                    0, self._h(start, goal), None)
            fringe.update(start_node, start_node.f)
            alt_paths = {}

            success = False
            while len(fringe) > 0:
                node, f = fringe.pop()

                if history[node.loc] < inf: continue
                if node.loc == goal:
                    path = deque()
                    while node != None:
                        path.appendleft(node.loc)
                        node = node.parent
                    individual_paths.append(path)
                    alternative_paths.append(alt_paths)
                    success = True
                    break

                for suc in self._successors(node.loc):
                    # create the node
                    x, y = suc
                    cost = self._c(node.loc, suc)
                    h = self._h(suc, goal)
                    nd = Node(x, y, cost, h, node)
                    if nd.f > fringe_score[suc]: continue

                    # find the alternative path
                    grid_backup_val = self.grid[node.loc]
                    self.grid[node.loc] = inf
                    if node.parent != None and node.parent.loc != suc:
                        pather = AStar(self.grid, node.parent.loc, suc)
                        success = pather.findpath()
                        if not success: continue
                        alt_paths[(node.parent.loc, node.loc, suc)] = pather.path
                    self.grid[node.loc] = grid_backup_val
 
                    # add to fringe
                    fringe.update(nd, nd.f)
                    fringe_score[nd.loc] = nd.f

            if not success: return False

        return True


    def _h(self, s, t):
        """
        Calculates the heuristic between 2 nodes, s and t.
        """
        x1, y1 = s
        x2, y2 = t
        return (abs(x1 - x2) + abs(y1 - y2)) * 10

    def _c(self, s, t):
        return max(self.grid[s], self.grid[t])


class MAPPTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10, 10, 10)

    def test_basic(self):
        starts = ((0, 0), (5, 0))
        goals = ((0, 5), (5, 5))
        pather = MAPP(self.grid, starts, goals)
        success = pather.findpath()
        self.assertTrue(success)
        
