from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.preprocessing import LabelBinarizer
import numpy as np
import unittest

class ChainClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, Y):
        # binarize labels
        self.bl = LabelBinarizer()
        Y = self.bl.fit_transform(Y)
        self.classes_ = self.bl.classes_
 
        # create an estimator for each label
        self.estimators_ = []
        for i in xrange(self.bl.classes_.shape[0]):
            estimator = clone(self.estimator)
            estimator.fit(np.concatenate((X, Y[:, :i]), axis=1), Y[:,i])
            self.estimators_.append(estimator)

    def predict(self, X):
        self._check_is_fitted()

        X = np.atleast_2d(X)
        Y = np.empty((X.shape[0], self.classes_.shape[0]))
        for i, estimator in enumerate(self.estimators_):
            Y[:,i] = estimator.predict(np.concatenate((X, Y[:, :i]), axis=1))

        return self.bl.inverse_transform(Y)

    def _check_is_fitted(self):
        if not hasattr(self, "estimators_"):
            raise ValueError("The object hasn't been fitted yet!")


class ChainClassifierTest(unittest.TestCase):
    def test_basic(self):
        from sklearn.svm import SVC
        X = ((1, 1, 0), (0, 1, 1), (1, 0, 1))
        Y = (('foo', 'bar'), ('bar', 'baz'), ('foo', 'baz'))
        clf = ChainClassifier(SVC())
        clf.fit(X, Y)
        predictions = clf.predict((1, 1, 1))
        self.assertIn('foo', predictions[0])
        self.assertIn('bar', predictions[0])
        self.assertIn('baz', predictions[0])

    def test_correlation(self):
        # TODO: write a test that test correlation between labels
        pass

