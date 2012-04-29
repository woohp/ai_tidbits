import heapq
import itertools

_REMOVED = '<removed>'

class PriorityQueue(object):
    def __init__(self):
        self.data = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def update(self, obj, priority):
        if obj in self.entry_finder:
            self.entry_finder[obj][-1] = _REMOVED
        count = next(self.counter)
        entry = [priority, count, obj]
        heapq.heappush(self.data, entry)
        self.entry_finder[obj] = entry

    def peek(self):
        while self.data[0][-1] is _REMOVED:
            heapq.heappop(self.data)
        return self.data[0][-1]

    def peek_priority(self):
        while self.data[0][-1] is _REMOVED:
            heapq.heappop(self.data)
        return self.data[0][0]

    def pop(self):
        while self.data[0][-1] is _REMOVED:
            heapq.heappop(self.data)
        priority, count, obj = heapq.heappop(self.data)
        del self.entry_finder[obj]
        return (obj, priority)

    def remove(self, obj):
        if obj in self.entry_finder:
            self.entry_finder[obj][-1] = _REMOVED
            del self.entry_finder[obj]

    def __contains__(self, obj):
        return obj in self.entry_finder
        
    def __len__(self):
        return len(self.entry_finder)

