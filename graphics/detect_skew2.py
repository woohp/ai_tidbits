import scipy as sp
from scipy.misc import imresize

def _hough_transform(img, angles):
    rows, cols = img.shape

    # determine the number of bins
    d = sp.ceil(sp.hypot(*img.shape))
    nr_bins = 2 * d
    bins = sp.linspace(-d, d, nr_bins)

    # create the accumulator
    out = sp.zeros((nr_bins, len(angles)), dtype=sp.float64)

    # compute the sines/cosines
    cos_theta = sp.cos(angles)
    sin_theta = sp.sin(angles)

    # constructe the x and y values
    y = []
    x = []
    for i in xrange(rows):
        y += [i] * cols
        x += range(cols)
    y = sp.array(y)
    x = sp.array(x)

    # flatten image
    flattened_img = img.flatten()

    for i, (c, s) in enumerate(zip(cos_theta, sin_theta)):
        distances = x * c + y * s
        bin_indices = (sp.round_(distances) - bins[0]).astype(sp.uint8)
        bin_sums = sp.bincount(bin_indices, flattened_img)
        out[:len(bin_sums), i] = bin_sums

    return out
        
def detect_skew(img, min_angle=-45, max_angle=45, resolution=0.1):
    img = sp.atleast_2d(img)
    rows, cols = img.shape

    min_target_size = 200
    min_size = min(rows, cols)
    target_size = min_target_size if min_size > min_target_size else min_size
    resize_ratio = float(target_size) / min_size
    img = imresize(img, resize_ratio)

    # determine the angles to do hough transform at
    num_samples = (max_angle - min_angle) / resolution
    min_angle_radian = min_angle * sp.pi / 180
    max_angle_radian = max_angle * sp.pi / 180
    angles = sp.linspace(min_angle_radian, max_angle_radian, num_samples)

    img *= -1
    img += 255
 
    # do the hough transfer
    hough_out = _hough_transform(img, angles)

    # determine which angle gives max variance
    variances = sp.var(hough_out, axis=0)
    max_variance_index = sp.argmax(variances)
    best_angle = min_angle + max_variance_index * resolution

    return best_angle

