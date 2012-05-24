import numpy as np
from scipy.signal import convolve2d

def hog(image, window_size, num_bins=9, overlap=True):
    height, width = image.shape

    # determine the windows locations
    if overlap:
        windows = [(slice(y//2, y//2+window_size), slice(x//2, x//2+window_size))
                 for y in xrange(0, height * 2 - window_size, window_size)
                 for x in xrange(0, width * 2 - window_size, window_size)]
    else:
        windows = [(slice(y, y+window_size), slice(x, x+window_size))
                 for y in xrange(0, height, window_size)
                 for x in xrange(0, width, window_size)]

    # do image convolution
    hx = np.atleast_2d([-1, 0, 1])
    hy = hx.T
    gx = convolve2d(image, hx, 'same')
    gy = convolve2d(image, hy, 'same')

    # compute the angles and magnitudes
    angles = np.arctan2(gy, gx)
    magnitudes = (gy ** 2 + gx ** 2) ** 0.5
    angle_range = (-np.pi, np.pi)

    # compute the descriptor
    descriptor = np.empty(len(windows) * num_bins)
    i = 0
    for slice_y, slice_x in windows:
        block, bin_edges = np.histogram(angles[slice_y, slice_x],
                num_bins, angle_range, weights=magnitudes[slice_y, slice_x])
        block /= (np.linalg.norm(block) + 0.01)
        descriptor[i:i+num_bins] = block
        i += num_bins

    return descriptor


#np.set_printoptions(linewidth=100000)
#a = np.zeros((14, 14))
#a[7,:] = 1
#hog(a, 7, overlap=False)

