import numpy as np
from scipy import ndimage
import sys
import json
from os.path import basename, splitext


"""
SI / TI calculations taken from:
https://github.com/slhck/siti

Author: Werner Robitza <werner.robitza@gmail.com>
Licensed without restrictions
"""

def calculate_si(frame_data):
    """
    Calculate SI of a frame.

    Arguments:
        - frame_data {ndarray}

    Keyword Arguments:
        - magnitude {bool} -- whether to use the magnitude-based calculation

    Returns:
        - {float}
    """
    sob_x = ndimage.sobel(frame_data, axis=0)
    sob_y = ndimage.sobel(frame_data, axis=1)
    si = np.hypot(sob_x, sob_y).std()
    return si


def calculate_ti(frame_data, previous_frame_data):
    """
    Calculate TI between two frames.

    Arguments:
        frame_data {ndarray} -- current frame
        previous_frame_data {ndarray} -- previous frame, must be of same size as current frame

    Returns:
        - {float}
    """
    return (frame_data - previous_frame_data).std()


def si_ti_calculation(filename, width, height):
    frame_size = width * height
    bit_max = 255
    si_values = []
    ti_values = [0.0]
    previous_frame_data = None

    with open(filename, 'rb') as f:
        luma = f.read(frame_size)
        chroma = f.read(frame_size // 2)
        while len(luma) > 0:
            frame_data = np.frombuffer(luma, dtype=np.uint8)
            frame_data = (frame_data.astype(np.float64) / bit_max).reshape(height, width)
            si_values.append(calculate_si(frame_data))
            if previous_frame_data is not None:
                ti_values.append(calculate_ti(frame_data, previous_frame_data))

            previous_frame_data = frame_data
            luma = f.read(frame_size)
            chroma = f.read(frame_size // 2)
    return si_values, ti_values



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python SI_TI_calculation.py filename")
    filename = sys.argv[1]
    width = 352
    height = 288
    si_orig, ti_orig = si_ti_calculation(filename, width, height)
    si = np.round(np.array(si_orig).astype(float), 3).tolist()
    ti = np.round(np.array(ti_orig).astype(float), 3).tolist()

    outfile = splitext(basename(filename))[0] + ".txt"
    with open(outfile, "w") as f:
        f.write("max_si: {}".format(round(np.max(si), 3)))
        f.write("max_ti: {}".format(round(np.max(ti), 3)))
