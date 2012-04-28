
def Node(object):
    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.g = g

    def make_successor(self, dx, dy):
        return Node(self.x + dx, self.y + dy, self.g + 10)

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
        y, x = s
        successors = []
        if self.grid.is_valid(y-1, x):
            successors.append((y-1, x))
        if self.grid.is_valid(y+1, x):
            successors.append((y+1, x))
        if self.grid.is_valid(y, x-1):
            successors.append((y, x-1))
        if self.grid.is_valid(y, x+1):
            successors.append((y, x+1))
        return successors


