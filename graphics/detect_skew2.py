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
        
def detect_skew(img, min_angle=-20, max_angle=20, quality='low'):
    img = sp.atleast_2d(img)
    rows, cols = img.shape
    min_min_angle = min_angle
    max_max_angle = max_angle

    if quality == 'low':
        resolution = sp.arctan2(2.0, cols) * 180.0 / sp.pi
        min_target_size = 100
        resize_order = 1
    elif quality == 'high':
        resolution = sp.arctan2(1.0, cols) * 180.0 / sp.pi
        min_target_size = 300
        resize_order = 3
    else:
        resolution = sp.arctan2(1.0, cols) * 180.0 / sp.pi
        min_target_size = 200
        resize_order = 2

    # resize the image so it's faster to work with
    min_size = min(rows, cols)
    target_size = min_target_size if min_size > min_target_size else min_size
    resize_ratio = float(target_size) / min_size
    img = imresize(img, resize_ratio)
    rows, cols = img.shape

    img *= -1
    img += 255

    while True:
        current_resolution = (max_angle - min_angle) / 30.0
        angles = sp.linspace(min_angle, max_angle, 31)

        # do the hough transfer
        hough_out = _hough_transform(img, angles * sp.pi / 180)
        
        # determine which angle gives max variance
        variances = sp.var(hough_out, axis=0)
        max_variance_index = sp.argmax(variances)
        best_angle = min_angle + max_variance_index * current_resolution

        if current_resolution < resolution:
            break

        # update the angle range
        min_angle = max(best_angle - current_resolution, min_min_angle)
        max_angle = min(best_angle + current_resolution, max_max_angle)

    return best_angle

