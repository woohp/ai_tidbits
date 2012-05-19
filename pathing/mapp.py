import sys
sys.path.append('.')
from utils.grid import *
from utils.priority_queue import *
from collections import deque
from pathing_base import *

inf = float('inf')

class MAPP(Pathing):
    def __init__(self, grid, starts, goals):
        self.grid = grid
        self.starts = starts
        self.goals = goals

    def findpath(self):
        pass

    
