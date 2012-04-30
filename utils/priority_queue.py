import heapq
import itertools
import unittest

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


if __name__ == '__main__':
    class PriorityQueueTest(unittest.TestCase):
        def test_simple(self):
            q = PriorityQueue()
            q.update(100, 3)
            q.update(1, 4)
            q.update(5, 1)
            q.update(4, 2)
            self.assertEqual(len(q), 4)
            self.assertIn(100, q)
            self.assertIn(1, q)
            self.assertIn(5, q)
            self.assertIn(4, q)
            self.assertEqual(q.peek(), 5)
            self.assertEqual(q.peek_priority(), 1)
            self.assertEqual(q.pop(), (5, 1))
            self.assertEqual(q.pop(), (4, 2))
            self.assertEqual(q.peek(), 100)
            self.assertEqual(q.peek_priority(), 3)
            self.assertEqual(q.pop(), (100, 3))
            self.assertEqual(len(q), 1)
            self.assertEqual(q.pop(), (1, 4))
            self.assertEqual(len(q), 0)
            with self.assertRaises(IndexError):
                q.pop()

        def test_remove(self):
            q = PriorityQueue()
            q.update(1, 1)
            q.update(2, 2)
            q.update(3, 3)
            q.update(4, 4)
            q.remove(3)
            self.assertNotIn(3, q)
            self.assertEqual(len(q), 3)
            self.assertEqual(q.pop(), (1, 1))
            self.assertEqual(q.pop(), (2, 2))
            self.assertEqual(q.pop(), (4, 4))

        def test_remove2(self):
            q = PriorityQueue()
            q.update(1, 1)
            q.remove(1)
            self.assertEqual(len(q), 0)
            with self.assertRaises(IndexError):
                q.pop()

        def test_replace(self):
            q = PriorityQueue()
            q.update(1, 1)
            q.update(2, 2)
            q.update(3, 3)
            q.update(1, 10)
            self.assertEqual(len(q), 3)
            self.assertEqual(q.peek(), 2)
            self.assertEqual(q.peek_priority(), 2)
            self.assertEqual(q.pop(), (2, 2))
            self.assertEqual(q.pop(), (3, 3))
            self.assertEqual(q.pop(), (1, 10))

    unittest.main()

