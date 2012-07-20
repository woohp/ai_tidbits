import scipy as sp
from scipy.ndimage import convolve

kernel_N = sp.array([[1], [-1], [0]])
kernel_S = sp.array([[0], [-1], [1]])
kernel_E = sp.array([[0, -1, 1]])
kernel_W = sp.array([[1, -1, 0]])

def g1(x, kappa):
    return sp.exp(-((x / kappa) ** 2))

def g2(x, kappa):
    return 1.0 / (1.0 + (x / kappa) ** 2)

def shift(img, dy, dx):
    rows, cols = img.shape
    result = sp.zeros(img.shape, dtype=img.dtype)
    result[max(dy, 0):rows+dy, max(dx, 0):cols+dx] = img[max(-dy, 0):rows-dy, max(-dx, 0):cols-dx]
    return result

def anistropic_diffusion(I, num_iter=15, delta=1.0/8, kappa=10, option=0):
    g = g1 if option == 0 else g2

    I_t = I.astype(sp.float64)
    for i in xrange(num_iter):
        gradient_N = shift(I_t, 0, 1)
        gradient_N -= I_t
        gradient_S = shift(I_t, 0, -1)
        gradient_S -= I_t
        gradient_E = shift(I_t, 1, 0)
        gradient_E -= I_t
        gradient_W = shift(I_t, -1, 0)
        gradient_W -= I_t

        c_N = g(sp.absolute(gradient_N), kappa)
        c_S = g(sp.absolute(gradient_S), kappa)
        c_E = g(sp.absolute(gradient_E), kappa)
        c_W = g(sp.absolute(gradient_W), kappa)
        
        I_t += delta * (c_N * gradient_N + c_S * gradient_S + c_E * gradient_E + c_W * gradient_W)

    return I_t

