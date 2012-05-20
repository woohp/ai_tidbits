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
        self.num_agents = len(starts)
        self.individual_paths = []
        self.alternative_paths = {}
        self.paths = []

    def findpath(self):
        # compute each path individually along with all the alternative paths
        # using a modified version of A*
        for start, goal in itertools.izip(self.starts, self.goals):
            history = Grid(self.grid.width, self.grid.height, False)
            fringe_score = Grid(self.grid.width, self.grid.height, inf)
            fringe = PriorityQueue()
            start_node = Node(start[0], start[1],
                    0, self._h(start, goal), None)
            fringe.update(start_node, start_node.f)

            success = False
            while len(fringe) > 0:
                node, f = fringe.pop()

                if history[node.loc]: continue
                history[node.loc] = True

                if node.loc == goal:
                    path = deque()
                    while node != None:
                        path.appendleft(node.loc)
                        node = node.parent
                    self.individual_paths.append(path)
                    success = True
                    break

                for suc in self._successors(node.loc):
                    # create the node
                    x, y = suc
                    cost = self._c(node.loc, suc)
                    h = self._h(suc, goal)
                    nd = Node(x, y, cost, h, node)
                    if nd.f >= fringe_score[suc] or history[nd.loc]: continue

                    # find the alternative path
                    if node.parent != None:
                        if not self.find_alternative_path(node.parent.loc, node.loc, suc):
                            continue
 
                    # add to fringe
                    fringe.update(nd, nd.f)
                    fringe_score[nd.loc] = nd.f
            
            if not success: return False

        self.paths = [[pos] for pos in self.starts]
        offcourse_paths = self.paths[:]

        current_positions = list(self.starts)
        current_positions_map = Grid(self.grid.width, self.grid.height, inf)
        for i, pos in enumerate(self.starts):
            current_positions_map[pos] = i
        prev_positions = [None] * self.num_agents # previous position in the individual paths
        visited_positions = [set() for i in xrange(self.num_agents)]
        reached_destinations = set()

        while len(reached_destinations) < self.num_agents:
            # do the progression step
            while True:
                changed = False
                moved = set()
                for i in xrange(len(current_positions)):
                    if i in reached_destinations: continue
                    if len(self.individual_paths[i]) == 1:
                        reached_destinations.add(i)
                        continue
                    if i in moved: continue

                    cur_pos = current_positions[i]
                    next_pos = self.individual_paths[i][1]
                    
                    if len(offcourse_paths[i]) > 1:
                        self.paths[i].append(cur_pos)
                    elif current_positions_map[next_pos] < i:
                        self.paths[i].append(cur_pos)
                    elif current_positions_map[next_pos] == inf:
                        current_positions[i] = next_pos
                        current_positions_map[cur_pos] = inf
                        current_positions_map[next_pos] = i
                        visited_positions[i].add(next_pos)
                        prev_positions[i] = cur_pos
                        self.paths[i].append(next_pos)
                        self.individual_paths[i].popleft()
                        offcourse_paths[i] = [next_pos]
                        changed = True
                    else:
                        if prev_positions[i] == None:
                            self.paths[i].append(cur_pos)
                            continue
 
                        # calculate the private zones of all higher priority agents
                        private_zones = set()
                        for j in xrange(i):
                            private_zones.add(current_positions[j])
                            private_zones.add(prev_positions[j])

                        # see if we can bring blank to the next position
                        can_bring_blank = False
                        alt_path = self.alternative_paths[(next_pos, cur_pos, prev_positions[i])]
                        for j, l in enumerate(alt_path):
                            if l in private_zones: break
                            if current_positions_map[l] == inf:
                                can_bring_blank = True
                                break
                            elif current_positions_map[l] in moved:
                                break
                        if not can_bring_blank: continue

                        # bring blank to the next position
                        for k in xrange(j, 0, -1):
                            pos = alt_path[k]
                            next_agent_index = current_positions_map[alt_path[k-1]]
                            assert next_agent_index > i # make sure that agent is of lower priority
                            current_positions[next_agent_index] = pos
                            current_positions_map[pos] = next_agent_index
                            self.paths[next_agent_index].append(pos)
                            offcourse_paths[next_agent_index].append(pos)
                            moved.add(next_agent_index)

                        # move current agent over there
                        current_positions[i] = next_pos
                        current_positions_map[cur_pos] = inf
                        current_positions_map[next_pos] = i
                        visited_positions[i].add(next_pos)
                        prev_positions[i] = cur_pos
                        self.paths[i].append(next_pos)
                        self.individual_paths[i].popleft()
                        offcourse_paths[i] = [next_pos]
                        changed = True

                if not changed: break

            # do the reposition step
            for i in xrange(self.num_agents-1, -1, -1):
                if i in reached_destinations: continue
                elif current_positions[i] in self.individual_paths[i]:
                    self.paths[i].append(self.paths[i][-1])
                else:
                    cur_pos = current_positions[i]
                    next_pos = offcourse_paths[i][-2]
                    if current_positions_map[next_pos] == inf:
                        current_positions[i] = next_pos
                        current_positions_map[cur_pos] = inf
                        current_positions_map[next_pos] = i
                        self.paths[i].append(next_pos)
                        offcourse_paths[i].pop()
                    else:
                        self.paths[i].append(cur_pos)

        return True

    def find_alternative_path(self, start, blackout, goal):
        if start == goal: return True
        if (start, blackout, goal) in self.alternative_paths: return True

        backup_val = self.grid[blackout]
        self.grid[blackout] = inf
        pather = AStar(self.grid, start, goal)
        success = pather.findpath()
        if success:
            self.alternative_paths[(start, blackout, goal)] = pather.path
            self.alternative_paths[(goal, blackout, start)] = deque(reversed(pather.path))
        self.grid[blackout] = backup_val
        return success


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

    def check_valid_path(self, starts, goals, paths, grid=None):
        # check that each path actually goes from start to goal
        if grid == None: grid = self.grid
        for start, goal, path in zip(starts, goals, paths):
            self.assertEqual(path[0], start)
            self.assertEqual(path[-1], goal)
            prev_x, prev_y = path[0]
            for x, y in path[1:]:
                self.assertLessEqual(abs(x-prev_x) + abs(y-prev_y), 1)
                prev_x = x
                prev_y = y

        # check no point-wise collision
        for state in zip(*paths):
            occupied = set()
            for loc in state:
                self.assertNotIn(loc, occupied)
                occupied.add(loc)

        # check pairwise collision
        for i in xrange(1, len(paths[0])):
            movements = set()
            for j in xrange(len(paths)):
                self.assertNotIn((paths[j][i], paths[j][i-1]), movements)
                movements.add((paths[j][i-1], paths[j][i]))


    def test_not_slidable(self):
        grid = Grid(10, 1, 10)
        starts = ((0, 0),)
        goals = ((9, 0),)
        pather = MAPP(grid, starts, goals)
        success = pather.findpath()
        self.assertFalse(success) 

    def test_basic(self):
        starts = ((0, 0), (5, 0))
        goals = ((0, 5), (5, 5))
        pather = MAPP(self.grid, starts, goals)
        success = pather.findpath()
        self.assertTrue(success)
        self.check_valid_path(starts, goals, pather.paths)

    def test_simple_collision(self):
        starts = ((0, 5), (9, 5))
        goals = ((9, 5), (0, 5))
        pather = MAPP(self.grid, starts, goals)
        success = pather.findpath()
        self.assertTrue(success)
        self.check_valid_path(starts, goals, pather.paths)
        
