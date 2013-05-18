from collections import defaultdict, deque
import unittest

_inf = float('inf')

class Graph(object):
    def __init__(self):
        self.capacity = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))
        self.height = defaultdict(int)
        self.excess = defaultdict(int)

    def add_edge(self, p, q, weight, undirected=False):
        self.capacity[p][q] = weight
        if undirected:
            self.capacity[q][p] = weight
        else:
            self.capacity[q][p] = 0

    def _push(self, u, v):
        send = min(self.excess[u], self.capacity[u][v] - self.flow[u][v])
        self.flow[u][v] += send
        self.flow[v][u] -= send
        self.excess[u] -= send
        self.excess[v] += send

    def _relabel(self, u):
        min_height = _inf
        for v, capacity in self.capacity[u].items():
            if capacity - self.flow[u][v] > 0 and self.height[v] < min_height:
                min_height = self.height[v]
                self.height[u] = min_height + 1
    
    def max_flow(self, source, sink):
        self.height[source] = len(self.capacity)
        self.excess[source] = _inf

        q = deque()
        in_queue = set()

        # initialize by pushing out from the source and then adding children to queue
        for v in self.capacity[source].keys():
            self._push(source, v)
            if v != sink:
                q.append(v)
                in_queue.add(v)

        # main loop
        while len(q):
            u = q.popleft()

            min_height = _inf
            for v, capacity in self.capacity[u].items():
                # try push
                if capacity - self.flow[u][v] > 0:
                    if self.height[u] > self.height[v]:
                        self._push(u, v)
                        if not v in in_queue and v != source and v != sink:
                            q.append(v)
                            in_queue.add(v)
                    if self.height[v] < min_height:
                        min_height = self.height[v]

            # relabel
            if self.excess[u] != 0:
                self.height[u] = min_height + 1
                q.appendleft(u)
            else:
                in_queue.remove(u)

        # calculate total flow
        total_flow = 0
        for v, flow in self.flow[sink].items():
            total_flow += flow
        return -total_flow


class MaxFlowGraphTest(unittest.TestCase):
    def test_simple(self):
        g = Graph()
        g.add_edge('s', 't', 5)
        flow = g.max_flow('s', 't')
        self.assertEqual(flow, 5)
        self.assertEqual(g.flow['s']['t'], 5)

    def test_simple_2(self):
        g = Graph()
        g.add_edge('s', 1, 5)
        g.add_edge('s', 2, 6)
        g.add_edge(1, 't', 3)
        g.add_edge(2, 't', 2)
        flow = g.max_flow('s', 't')
        self.assertEqual(flow, 5)
        self.assertEqual(g.flow['s'][1], 3)
        self.assertEqual(g.flow['s'][2], 2)
        self.assertEqual(g.flow[1]['t'], 3)
        self.assertEqual(g.flow[2]['t'], 2)

    def test_3(self):
        g = Graph()
        g.add_edge('s', 1, 1000)
        g.add_edge('s', 2, 1000)
        g.add_edge(1, 2, 1)
        g.add_edge(1, 't', 1000)
        g.add_edge(2, 't', 1000)
        flow = g.max_flow('s', 't')
        self.assertEqual(flow, 2000)

