import sys
sys.path.append('.')
import numpy as np
from utils import *
from sklearn.utils import resample, shuffle
import unittest
from sklearn.datasets import fetch_mldata


def linear_kernel(i, j):
    return np.dot(i, j)

def make_poly_kernel(degree, coef0):
    def kernel(i, j):
        return (np.dot(i, j) + coef0) ** degree
    return kernel

def make_rbf_kernel(gamma):
    def kernel(i, j):
        d = a - b
        return np.exp(-gamma * np.dot(d, d))
    return kernel

def intersection_kernel(i, j):
    return np.sum(np.minimum(i, j))



class LASVM(object):
    def __init__(self, C=1, tau=0.001, kernel='linear', degree=3, gamma=0.0, coef0=0.0):
        self.data = None
        self.S = set() # the support vectors
        self.alpha = {}
        self.g = {}
        self.y = {}
        self.C = C
        self.tau = tau
        self.b = 0

        if kernel == 'linear':
            self._kernel = linear_kernel
        elif kernel == 'poly':
            self._kernel = make_poly_kernel(degree, coef0)
        elif kernel == 'rbf':
            self._kernel = make_rbf_kernel(gamma)
        elif kernel == 'intersection':
            self._kernel = intersection_kernel
        else:
            self._kernel = kernel
            

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
        
        if not self.is_violating(i, j):
            return
        
        lamb = min((self.g[i] - self.g[j]) / (self.kernel(i, i) + self.kernel(j, j) - 2 * self.kernel(i, j)),
                self.B(i) - self.alpha[i], self.alpha[j] - self.A(j))
        self.alpha[i] += lamb
        self.alpha[j] -= lamb
        for s in self.S:
            self.g[s] -= lamb * (self.kernel(i, s) - self.kernel(j, s))

    def reprocess(self):
        i = argmax(self.S, lambda s: self.g[s], lambda s: self.alpha[s] < self.B(s))
        j = argmin(self.S, lambda s: self.g[s], lambda s: self.alpha[s] > self.A(s))

        if not self.is_violating(i, j):
            return 0.0

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
            self.S.remove(s)
            del self.y[s]
            del self.g[s]
            del self.alpha[s]

        self.b = (self.g[i] + self.g[j]) / 2

        return delta

    def kernel(self, i, j):
        return self._kernel(self.data[i], self.data[j])

    def A(self, s):
        return min(0, self.y[s] * self.C)

    def B(self, s):
        return max(0, self.y[s] * self.C)

    def is_violating(self, i, j):
        return self.alpha[i] < self.B(i) and self.alpha[j] > self.A(j) and self.g[i] - self.g[j] > self.tau

    def predict(self, X):
        Y_predict = [sum(self._kernel(self.data[s], x) * self.alpha[s] for s in self.S) + self.b for x in X]
        return np.sign(Y_predict)

    def fit(self, X, Y):
        num_examples = len(X)
        data_indices = np.arange(num_examples)
        self.data = X
        Y = np.array(Y, dtype=float)

        sample = resample(data_indices, replace=False, n_samples=min(20, num_examples), random_state=0)
        for i in sample:
            y = Y[i]
            self.S.add(i)
            self.y[i] = y
            self.alpha[i] = 0.0
            self.g[i] = y
       

        for i in xrange(5):
            min_delta = 999999999
            for i in data_indices:
                self.process(i, Y[i])
                delta = self.reprocess()
                min_delta = min(min_delta, delta)
            if min_delta < self.tau: break

            data_indices = shuffle(data_indices)

        while True:
            delta = self.reprocess()
            if delta < self.tau: break


class LASVMTest(unittest.TestCase):
    def test_basic_1D(self):
        X = [-4, -2, -1, 2, 3, 4, 5, 7, 8, 9]
        Y = [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
        svm = LASVM(C=10, tau=0.001)
        svm.fit(X, Y)

        predictions = svm.predict([-6, 3.4, 4.6, 10])
        self.assertEqual([-1, -1, 1, 1], predictions.tolist())


    def test_basic_2D(self):
        X = [[1, 2], [2, 1], [2, 3], [2, 4], [10, 11], [11, 15], [3, 1], [6, 4], [20, 10], [8, 7], [9, 1]]
        Y = [-1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
        svm = LASVM(C=10, tau=0.001)
        svm.fit(X, Y)

        predictions = svm.predict([[100, 99], [99, 100], [1, 1.1], [4.01, 4]])
        self.assertEqual([1, -1, -1, 1], predictions.tolist())


    def test_basic_poly(self):
        X = [-4, -3, -2, 1, 0, 1, 2, 3, 4]
        Y = [-1, -1, 1, 1, 1, 1, -1, -1, -1]
        svm = LASVM(C=100, tau=0.001, kernel='poly', degree=2, coef0=1)
        svm.fit(X, Y)

        predictions = svm.predict([-5, -2.7, -2.3, 0.01, 1.3, 1.6, 5])
        self.assertEqual([-1, -1, 1, 1, 1, -1, -1], predictions.tolist())


    def test_mnist(self):
        mnist = fetch_mldata('MNIST original')
        X, Y = resample(mnist.data, mnist.target, replace=False, n_samples=1000, random_state=0)
        X = X.astype(float)
        Y = [1 if y == 0 else -1 for y in Y]

        svm = LASVM(C=10, tau=0.001)
        svm.fit(X, Y)

        X_test, Y_test = resample(mnist.data, mnist.target, replace=False, n_samples=300, random_state=2)
        X_test = X_test.astype(float)
        Y_test = [1 if y == 0 else -1 for y in Y_test]
        Y_predict = svm.predict(X_test)
        percent_correct = np.sum(Y_predict == Y_test) / 300.0

        self.assertGreater(percent_correct, 0.95)

