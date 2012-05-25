import sys
import pickle
import numpy as np
from sklearn import datasets, svm, utils, preprocessing
from hog import hog

import unittest

class DigitClassifier(object):
    def __init__(self, classifier=svm.SVC(kernel='linear', C=10)):
        self.clf = classifier

    def fit(self, X, Y):
        assert X.shape[1] == 28 * 28
        X = [self.compute_features(x) for x in X]
        self.clf.fit(X, Y)

    def predict(self, X):
        assert X.shape[1] == 28 * 28
        X = [self.compute_features(x) for x in X]
        return self.clf.predict(X)

    def score(self, X, Y):
        assert X.shape[1] == 28 * 28
        X = [self.compute_features(x) for x in X]
        return self.clf.score(X, Y)

    def compute_features(self, x):
        x = x.reshape(28, 28)
        return np.concatenate((hog(x, 4, num_bins=12), hog(x, 7, num_bins=12), hog(x, 14, num_bins=12)))


class DigitClassifierTest(unittest.TestCase):
    def test_mnist(self):
        mnist = datasets.fetch_mldata('MNist original')
        Xdata, Ydata = utils.shuffle(mnist.data, mnist.target, random_state=0)

        num_train = 500
        num_test = min(len(Xdata) - num_train, num_train)

        classifier = DigitClassifier()
        classifier.fit(Xdata[:num_train], Ydata[:num_train])
        score = classifier.score(Xdata[-num_test:], Ydata[-num_test:])
        self.assertGreater(score, 0.95)

