import sys
sys.path.append('.')
from utils.max_flow import Graph
import unittest

def denoise(img, smoothing):
    height = len(img)
    width = len(img[0])

    graph = Graph()
    for y in xrange(height):
        for x in xrange(width):
            graph.add_edge('s', (y, x), int(img[y][x] > 0))
            graph.add_edge((y, x), 't', abs(1 - img[y][x]))

            if y > 0:
                graph.add_edge((y-1, x), (y, x), smoothing * abs(img[y][x] - img[y-1][x]), undirected=True)
            if x > 0:
                graph.add_edge((y, x), (y, x-1), smoothing * abs(img[y][x] - img[y][x-1]), undirected=True)
            if y < height-1:
                graph.add_edge((y, x), (y+1, x), smoothing * abs(img[y][x] - img[y+1][x]), undirected=True)
            if x < width-1:
                graph.add_edge((y, x), (y, x+1), smoothing * abs(img[y][x] - img[y][x+1]), undirected=True)

    graph.max_flow('s', 't')
    ret = []
    for y in xrange(height):
        row = []
        for x in xrange(width):
            row.append(int(graph.nodes['s'][(y, x)] > 0))
        ret.append(row)

    return ret


class DenoiseTest(unittest.TestCase):
    def test_basic(self):
        img = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        img = denoise(img, 0.5)
        self.assertEqual(img, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_basic2(self):
        img = [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]]
        img = denoise(img, 0.3)
        self.assertEqual(img, [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]])

    def test_basic3(self):
        img = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
        img = denoise(img, 0.3)
        self.assertEqual(img, [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]])

