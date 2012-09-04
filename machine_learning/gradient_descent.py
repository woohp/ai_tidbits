import unittest


def gradient_descent(f, grad_f, starts, eps, precision=0.00001):
    while True:
        old = starts
        gradient = grad_f(starts)
        starts -= eps * gradient

        if abs(starts - old) < precision: break

    return starts


def negate(f):
    return lambda x: -f(x)

def numerical_gradient(f, eps=0.00001):
    diff = 2 * eps
    return lambda x: (f(x+eps) - f(x-eps)) / diff


class GradientDescentTest(unittest.TestCase):
    def test_x_squared(self):
        f = lambda x: x ** 2
        grad_f = lambda x: 2 * x
        starts = 5
        eps = 0.01

        min_x = gradient_descent(f, grad_f, starts=starts, eps=eps)
        self.assertAlmostEqual(0.0, min_x, places=3)

    def test_x_squared_with_numerical_gradient(self):
        f = lambda x: x ** 2
        grad_f = numerical_gradient(f)
        starts = 5
        eps = 0.01

        min_x = gradient_descent(f, grad_f, starts=starts, eps=eps)
        self.assertAlmostEqual(0.0, min_x, places=3)

    def test_grad_ascent(self):
        f = lambda x: -3 * x ** 3 - 6 * x ** 2 + 10 * x
        f = negate(f)
        grad_f = numerical_gradient(f)
        starts = 3
        eps = 0.01

        max_x = gradient_descent(f, grad_f, starts=starts, eps=eps)
        expected_max_x = (14 ** 0.5 - 2) / 3
        self.assertAlmostEqual(expected_max_x, max_x, places=3)

