import sys
from grid import *
from priority_queue import *
from collections import deque
from pathing_base import *

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
        self.U.push(goal, self._calculate_key(goal))

    def findpath(self):
        while self.U.peek_priority() < self._calculate_key(self.start) or self.rhs[self.start] != self.g[self.start]:
            u, kold = self.U.pop()
            if kold < self._calculate_key(u):
                self.U.push(u, self._calculate_key(u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for pred in self._successors(u):
                    self.update(pred)
            else:
                self.g[u] = inf
                self.update(u)
                for pred in self._successors(u):
                    self.update(pred)

    def update(self, u):
        if u != self.goal:
            self.rhs[u] = min((self._c(u, s) + self.g[s] for s in self._successors(u)))
        self.U.remove(u)
        if self.g[u] != self.rhs[u]:
            self.U.push(u, self._calculate_key(u))

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


if __name__ == '__main__':
    grid = Grid(10, 10, 10)
    pather = DStarLite(grid, (1, 1), (8, 3))
    pather.findpath()
    print 'path:', pather.next_move()
    print 'path:', pather.next_move()
    grid[5, 1] = 50
    pather.update((5, 1))
    grid[5, 2] = 50
    pather.update((5, 2))
    pather.findpath()
    while pather.current_move() != (8, 3):
        print 'path:', pather.next_move()

