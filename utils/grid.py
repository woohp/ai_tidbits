
class Grid(object):
    '''
    A simple 2D grid class
    '''
    def __init__(self, width, height, val=0):
        assert width > 0 and height > 0, 'width and height must be greater than 0'

        self.height = height
        self.width = width
        self.data = [val] * (width * height)

    def __getitem__(self, key):
        x, y = key
        return self.data[y*self.width+x]

    def __setitem__(self, key, item):
        x, y = key
        self.data[y*self.width+x] = item

    def is_valid(self, x, y):
        return y >= 0 and y < self.height and x >= 0 and x < self.width and self[x, y] >= 0

    def __repr__(self):
        s = '['
        for y in xrange(self.height):
            if y > 0:
                s += ' '
            for x in xrange(self.width):
                s += self[x, y].__repr__() + ' '
            if y == self.height - 1:
                s += ']'
            else:
                s += '\n'
        return s

