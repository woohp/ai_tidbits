import scipy as sp
from scipy.ndimage.interpolation import rotate
from scipy.misc import imresize

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

    # pad the image and invert the colors
    img *= -1
    img += 255
    padded_img = sp.zeros((rows*2, cols*2))
    padded_img[rows//2:rows//2+rows, cols//2:cols//2+cols] = img
    img = padded_img

    # keep dividing the interval in half to achieve O(log(n))
    while True:
        current_resolution = (max_angle - min_angle) / 30.0
        best_angle = None
        best_variance = 0.0

        # rotate the image, sum the pixel values in each row for each rotation
        # then find the variance of all the sums, pick the highest variance
        for i in xrange(31):
            angle = min_angle + i * current_resolution
            rotated_img = rotate(img, angle, reshape=False, order=resize_order)
            num_black_pixels = sp.sum(rotated_img, axis=1)
            variance = sp.var(num_black_pixels)
            if variance > best_variance:
                best_angle = angle
                best_variance = variance

        if current_resolution < resolution:
            break

        # update the angle range
        min_angle = max(best_angle - current_resolution, min_min_angle)
        max_angle = min(best_angle + current_resolution, max_max_angle)

    return best_angle

