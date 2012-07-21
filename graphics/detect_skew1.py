import scipy as sp
from scipy.ndimage.interpolation import rotate
from scipy.misc import imresize
import cv2

def detect_skew(img, min_angle=-45, max_angle=45):
    rows, cols = img.shape

    # resize the image so it's faster to work with
    min_size = min(rows, cols)
    new_min_size = 100 if min_size > 100 else min_size
    resize_ratio = float(new_min_size) / min_size
    print resize_ratio
    img = imresize(img, resize_ratio)
    rows, cols = img.shape

    # pad the image
    img = sp.zeros(img.shape) + 255 - img # flip the image
    padded_img = sp.zeros((rows*2, cols*2))
    padded_img[rows//2:rows//2+rows, cols//2:cols//2+cols] = img
    img = padded_img

    # rotate the image by various degrees, see which angle gives highest var
    best_variance = 0
    for angle in xrange(min_angle, max_angle+1):
        rotated_img = rotate(img, angle, reshape=False, order=1)
        num_black_pixels = sp.sum(rotated_img, axis=1) / cols
        variance = sp.var(num_black_pixels)
        if variance > best_variance:
            best_angle = angle
            best_variance = variance
        print angle, variance

    print 'best:', best_angle
        

detect_skew(cv2.imread('/media/sf_dev/scan2.png', 0))
