#!/usr/bin/env python
from PriorityQueue import PriorityQueue
from collections import deque
import sys
import random

inf = float('inf')


class Agent(object):
    """ An agent that participates in cooperative pathing with other agents.
    To use it, set the goal variable of all the agents, and call findpaths,
    passing in the entire collection of agents. findpaths will set the path
    variable if a path can be found for that agent."""
    def __init__(self, loc):
        self.loc = loc
        self.goal = None
        self.path = None
    
    def __repr__(self):
        return "[PathingAgent loc: %s, goal: %s, path: %s]" % (str(self.loc), str(self.goal), str(self.path))


class BFS(object):
    """ A class for resumable bfs
    Given a starting location and a map,
    you can continually query the distance to goal locations."""
    def __init__(self, m, start):
        self.m = m
        self.num_rows = len(m)
        self.num_cols = len(m[0])
        self.costs = {}
        self.fringe = deque()
        self.closed = set()
        self.fringe.append((start, 0))
        self.closed.add(start)

    def _search(self, goal):
        while len(self.fringe) > 0:
            current, cost = self.fringe.popleft()
    
            self.costs[current] = cost
            if current == goal:
                break
    
            y, x = current
            suc = (y, (x+1)%self.num_cols)
            if suc not in self.closed and self.m[suc[0]][suc[1]] != WATER:
                self.fringe.append((suc, cost + 1))
                self.closed.add(suc)
            suc = (y, (x-1)%self.num_cols)
            if suc not in self.closed and self.m[suc[0]][suc[1]] != WATER:
                self.fringe.append((suc, cost + 1))
                self.closed.add(suc)
            suc = ((y+1)%self.num_rows, x)
            if suc not in self.closed and self.m[suc[0]][suc[1]] != WATER:
                self.fringe.append((suc, cost + 1))
                self.closed.add(suc)
            suc = ((y-1)%self.num_rows, x)
            if suc not in self.closed and self.m[suc[0]][suc[1]] != WATER:
                self.fringe.append((suc, cost + 1))
                self.closed.add(suc)

    def get_cost(self, goal):
        if goal not in self.costs:
            self._search(goal)
        if goal not in self.costs: return inf
        return self.costs[goal]

def findpaths(agents, m, window=32):
    bfs_results = []
    num_rows = len(m)
    num_cols = len(m[0])

    requests = [(agent, BFS(m, agent.goal)) for agent in agents]
    random.shuffle(requests)
    reservations = set()

    for agent, bfs in requests:
        fringe = PriorityQueue()
        fringe_set = set()
        closed = set()
        
        # node is a tuple of ((location, g), parent_node), g is also the time
        # define a point as a tuple of (loc, g)
        fringe.push(((agent.loc, 0), None), bfs.get_cost(agent.loc))
        fringe_set.add((agent.loc, 0))

        path = None
        while len(fringe) > 0:
            f, node = fringe.pop()
            point, parent = node
            loc, g = point

            if point in closed or point in reservations:
                continue
            if parent != None:
                parent_point = parent[0]
                parent_loc, parent_g = parent_point
                if (parent_loc, g) in reservations and (loc, g - 1) in reservations:
                    continue
            closed.add(point)

            if g == window:
                path = deque()
                while parent != None:
                    path.appendleft(point)
                    point, parent = parent
                break

            y, x = loc
            suc = ((y, (x+1)%num_cols), g + 1)
            if suc not in fringe_set and m[suc[0][0]][suc[0][1]] != WATER:
                fringe.push((suc, node), g + 1 + bfs.get_cost(suc[0]))
                fringe_set.add(suc)
            suc = ((y, (x-1)%num_cols), g + 1)
            if suc not in fringe_set and m[suc[0][0]][suc[0][1]] != WATER:
                fringe.push((suc, node), g + 1 + bfs.get_cost(suc[0]))
                fringe_set.add(suc)
            suc = (((y+1)%num_rows, x), g + 1)
            if suc not in fringe_set and m[suc[0][0]][suc[0][1]] != WATER:
                fringe.push((suc, node), g + 1 + bfs.get_cost(suc[0]))
                fringe_set.add(suc)
            suc = (((y-1)%num_rows, x), g + 1)
            if suc not in fringe_set and m[suc[0][0]][suc[0][1]] != WATER:
                fringe.push((suc, node), g + 1 + bfs.get_cost(suc[0]))
                fringe_set.add(suc)
            suc = (loc, g + 1)
            if suc not in fringe_set and m[suc[0][0]][suc[0][1]] != WATER:
                fringe.push((suc, node), g + 1 + bfs.get_cost(suc[0]))
                fringe_set.add(suc)

        for point in path:
            reservations.add(point)
        agent.path = deque()
        for node in path:
            agent.path.append(node[0])


def getdist(start, goal, m):
    num_rows = len(m)
    num_cols = len(m[0])
    
    def h(n):
        row1, col1 = n
        row2, col2 = goal
        d_col = min(abs(col1 - col2), num_cols - abs(col1 - col2))
        d_row = min(abs(row1 - row2), num_rows - abs(row1 - row2))
        return d_row + d_col

    
    fringe = PriorityQueue()
    closed = set()
    fringe.push((start, 0), h(start))

    while len(fringe) > 0:
        f, (node, g) = fringe.pop()

        if node in closed: continue
        closed.add(node)
        if node == goal: return g
        
        y, x = node
        suc = (y, (x+1)%num_cols)
        if m[suc[1]][suc[0]] != WATER:
            fringe.push((suc, g+1), g+1+h(suc))
        suc = (y, (x-1)%num_cols)
        if m[suc[1]][suc[0]] != WATER:
            fringe.push((suc, g+1), g+1+h(suc))
        suc = ((y+1)%num_rows, x)
        if m[suc[1]][suc[0]] != WATER:
            fringe.push((suc, g+1), g+1+h(suc))
        suc = ((y-1)%num_rows, x)
        if m[suc[1]][suc[0]] != WATER:
            fringe.push((suc, g+1), g+1+h(suc))

    return inf



if __name__ == '__main__':

    m = [[0 for x in xrange(10)] for y in xrange(10)]
    agents = [PathingAgent((0, 0)), PathingAgent((0, 3))]
    agents[0].goal = (0, 3)
    agents[1].goal = (0, 0)

    paths = findpaths(agents, m, 6)

#    print getdist((0, 0), (4, 4), m)
    for agent in agents:
        print agent.path

