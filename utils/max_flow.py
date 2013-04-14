from collections import defaultdict, deque
import unittest

# implementation of the standard dinic algorithm
# not the most efficient implementation out there

class Graph(object):
    def __init__(self):
        self.nodes = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, p, q, weight):
        self.nodes[p][q] = weight

    def max_flow(self, source, sink):
        total_flow = 0

        while True:
            fringe = deque([(source, None)])
            history = set()
            path = None

            while len(fringe):
                node, parent = fringe.popleft()
                if node in history: continue
                history.add(node)

                if node == sink:
                    # create the path first and find the minimum capacity
                    path = deque([node])
                    min_weight = None
                    while parent is not None:
                        parent_node, parent = parent
                        path.appendleft(parent_node)
                        weight = self.nodes[parent_node][node]
                        if min_weight is None or weight < min_weight:
                            min_weight = weight
                        node = parent_node

                    total_flow += min_weight

                    # update resididual capacity
                    for i in xrange(len(path) - 1):
                        node1 = path[i]
                        node2 = path[i+1]
                        self.nodes[node1][node2] -= min_weight
                        self.nodes[node2][node1] += min_weight
                        self.flow[node1][node2] += min_weight

                    break

                for neighbor, weight in self.nodes[node].items():
                    if neighbor in history or weight <= 0: continue
                    fringe.append((neighbor, (node, parent)))
            
            if path is None:
                break

        return total_flow


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

