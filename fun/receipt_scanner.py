import sys
sys.path.append('.')
sys.path.append('..')

from skimage.measure import find_contours
from skimage.io import imread
from skimage.color import rgb2grey
from skimage.filter import threshold_otsu
import matplotlib.pyplot as plt
import scipy as sp
from scipy.ndimage.interpolation import rotate
from scipy.misc import imresize

from graphics.detect_skew1 import detect_skew

def scan_receipt(img, clf):
    angle_to_rotate = detect_skew(img, quality='medium')
    print 'angle_to_rotate', angle_to_rotate
    img = rotate(img, angle_to_rotate, order=5, cval=1.0)

    thresh = threshold_otsu(img)
    img = img < thresh

#    plt.imshow(img, interpolation='nearest', cmap='gray')
#    plt.axis('image')
#    plt.xticks([])
#    plt.yticks([])
#    plt.show()

    # extract individual lines
    num_blacks = sp.sum(img, axis=1)
    has_characters = num_blacks > 0.01 * img.shape[1]
    line_diffs = sp.ediff1d(has_characters.astype(sp.int32))
    line_starts = sp.nonzero(line_diffs == 1)[0]
    line_ends = sp.nonzero(line_diffs == -1)[0] + 2
    line_heights = line_ends - line_starts

    normal_line_height = sp.median(line_heights)
    lines = []
    for start, end, height in zip(line_starts, line_ends, line_heights):
        if height < normal_line_height * 1.2 and height > 5:
            lines.append(img[start:end])

    receipt_content = ''

    # extract individual characters from lines
    for line in lines:
        line_content = ''

        num_blacks = sp.sum(line, axis=0)
        has_character = num_blacks > 0
        col_diffs = sp.ediff1d(has_character.astype(sp.int32))
        col_starts = sp.nonzero(col_diffs == 1)[0]
        col_ends = sp.nonzero(col_diffs == -1)[0] + 2
        char_widths = col_ends - col_starts
        normal_char_width = sp.median(char_widths)
        min_char_width = normal_char_width * 0.8
        max_char_width = normal_char_width * 1.2

        # account for cases when 2 chars are merged, or if a single char is separated
        chars = []
        i = 0
        while i < len(col_starts):
            start = col_starts[i]
            end = col_ends[i]
            width = end - start

            if width < min_char_width:
                while i + 1 < len(col_starts):
                    expanded_width = col_ends[i+1] - start

                    if expanded_width < min_char_width:
                        i += 1
                    elif expanded_width > max_char_width:
                        break
                    elif col_starts[i+1] - end >= 3:
                        break
                    else:
                        i += 1
                        break

                chars.append(line[:, start:col_ends[i]])
            elif width >= normal_char_width * 2:
                chars.append(line[:, start:start+width//2-1])
                chars.append(line[:, start+width//2+1:end])
            else:
                chars.append(line[:, start:end])

            i += 1
        
        # pad each char to a square and resize it to 24x24
        padded_chars = []
        for char in chars:
            height, width = char.shape
            if height > width:
                diff = height - width
                pad_left = diff // 2
                padded_char = sp.zeros((height, height))
                padded_char[:, pad_left:pad_left+width] = char
            elif width > height:
                diff = width - height
                pad_top = diff // 2
                padded_char = sp.zeros((width, width))
                padded_char[pad_top:pad_top+height, :] = char

            final_char = imresize(padded_char, (25, 25), 'bicubic')

            padded_chars.append(final_char)

        for char in padded_chars:
            plt.imshow(char, interpolation='nearest', cmap='gray')
            plt.axis('image')
            plt.xticks([])
            plt.yticks([])
            plt.show()




img = imread('receipt1.png')
gray_img = rgb2grey(img)
scan_receipt(gray_img.copy(order='C'), None)
