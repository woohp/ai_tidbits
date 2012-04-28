import heapq
import itertools

class PriorityQueue(object):
    def __init__(self):
        self.data = []
        self.counter = itertools.count()

    def push(self, obj, priority):
        count = next(self.counter)
        heapq.heappush(self.data, (priority, count, obj))

    def peek(self):
        return self.data[0][2]

    def peek_priority(self):
        return self.data[0][0]

    def pop(self):
        entry = heapq.heappop(self.data)
        return (entry[2], entry[0])

    def remove(self, obj):
        for i in xrange(len(self.data)):
            if self.data[i][2] == obj:
                self.data.remove(self.data[i])
                return

    def __contains__(self, obj):
        for i in xrange(len(self.data)):
            if self.data[i][2] == obj:
                return True
        return False
        
    def __len__(self):
        return len(self.data)

