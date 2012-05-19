
inf = float('inf')

class Pathing(object):
    def __init__(self):
        pass

    def findpath(self, start, goal):
        pass

    def current_move(self):
        pass

    def next_move(self):
        pass

    def _successors(self, s):
        x, y = s
        successors = []
        if self.grid.is_valid(x, y-1):
            successors.append((x, y-1))
        if self.grid.is_valid(x, y+1):
            successors.append((x, y+1))
        if self.grid.is_valid(x-1, y):
            successors.append((x-1, y))
        if self.grid.is_valid(x+1, y):
            successors.append((x+1, y))
        return successors


