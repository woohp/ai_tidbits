import scipy as sp
from scipy.ndimage import convolve
import cv2

kernel_N = sp.array([[1], [-1], [0]])
kernel_S = sp.array([[0], [-1], [1]])
kernel_E = sp.array([[0, -1, 1]])
kernel_W = sp.array([[1, -1, 0]])

def g(x, kappa):
    return sp.exp(-((x / kappa) ** 2))

def shift(img, dx, dy):
    rows, cols = img.shape
    result = sp.zeros(img.shape, dtype=img.dtype)
    result[max(dy, 0):rows+dy, max(dx, 0):cols+dx] = img[max(-dy, 0):rows-dy, max(-dx, 0):cols-dx]
    return result

def anistropic_diffusion(I, num_iter=15, delta=1.0/8, kappa=10):
    I_t = I.astype(sp.float64)
    for i in xrange(num_iter):
        gradient_N = convolve(I_t, kernel_N)
        gradient_S = convolve(I_t, kernel_S)
        gradient_E = convolve(I_t, kernel_E)
        gradient_W = convolve(I_t, kernel_W)
        c_N = g(sp.absolute(gradient_N), kappa)
        c_S = g(sp.absolute(gradient_S), kappa)
        c_E = g(sp.absolute(gradient_E), kappa)
        c_W = g(sp.absolute(gradient_W), kappa)
        
        I_t += delta * (c_N * gradient_N + c_S * gradient_S + c_E * gradient_E + c_W * gradient_W)

    return I_t

