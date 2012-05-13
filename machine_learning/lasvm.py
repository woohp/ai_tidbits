import sys
sys.path.append('.')
from collections import defaultdict
from utils import *

class LASVM(object):
    def __init__(self, C=1):
        self.S = set() # the support vectors
        self.alpha = {}
        self.g = {}
        self.y = {}
        self.C = C

    def process(self, k, y):
        if k in self.S: return

        self.y[k] = y

        self.alpha[k] = 0.0
        self.g[k] = y - sum((self.alpha[s] * self.kernel(k, s) for s in self.S))
        self.S.add(k)

        if y == 1:
            i = k
            j = argmin(self.S, lambda s: self.g[s], lambda s: self.alpha[s] > self.A(s))
        else:
            j = k
            i = argmax(self.S, lambda s: self.g[s], lambda s: self.alpha[s] < self.B(s))
        
        if not self._is_violating(i, j): return
        
        lamb = min((self.g[i] - self.g[j]) / (self.kernel(i, i) + self.kernel(j, j) - 2 * self.kernel(i, j)),
                self.B(i) - self.alpha[i], self.alpha[j] - self.A(j))
        self.alpha[i] += lamb
        self.alpha[j] -= lamb
        for s in self.S:
            self.g[s] -= lamb * (self.kernel(i, s) - self.kernel(j, s))

    def reprocess(self):
        i = argmax(self.S, lambda s: self.g[s], lambda s: self.alpha[s] < self.B(s))
        j = argmin(self.S, lambda s: self.g[s], lambda s: self.alpha[s] > self.A(s))

        if not self._is_violating(i, j): return 0.0

        lamb = min((self.g[i] - self.g[j]) / (self.kernel(i, i) + self.kernel(j, j) - 2 * self.kernel(i, j)),
                self.B(i) - self.alpha[i], self.alpha[j] - self.A(j))
        self.alpha[i] += lamb
        self.alpha[j] -= lamb
        for s in self.S:
            self.g[s] -= lamb * (self.kernel(i, s) - self.kernel(j, s))

        i = argmax(self.S, lambda s: self.g[s], lambda s: self.alpha[s] < self.B(s))
        j = argmin(self.S, lambda s: self.g[s], lambda s: self.alpha[s] > self.A(s))

        delta = self.g[i] - self.g[j]

        toRemove = set()
        for s in self.S:
            if self.alpha[s] == 0.0:
                if self.y[s] == -1 and self.g[s] >= self.g[i]:
                    toRemove.add(s)
                elif self.y[s] == 1 and self.g[s] <= self.g[j]:
                    toRemove.add(s)
        for s in toRemove:
            print 'removed', s
            self.S.remove(s)
            del self.y[s]
            del self.g[s]
            del self.alpha[s]

#        b = (self.g[i] + self.g[j]) / 2

        return delta

    def A(self, s):
        return min(0, self.y[s] * self.C)

    def B(self, s):
        return max(0, self.y[s] * self.C)

    def kernel(self, i, j):
        return i * j

    def _is_violating(self, i, j):
        return self.alpha[i] < self.B(i) and self.alpha[j] > self.A(j) and self.g[i] - self.g[j] > 0.00001

if __name__ == '__main__':
    svm = LASVM(C=10)
    svm.process(-10, -1)
    svm.process(10, 1)
    for i in xrange(6, 1, -1):
        svm.process(-i, -1);
        svm.reprocess();
        svm.process(i, 1);
        svm.reprocess();

    while True:
        if svm.reprocess() < 0.1: break
    print 'S', svm.S
    print 'g', svm.g
    print 'alpha', svm.alpha

