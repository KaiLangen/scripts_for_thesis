import numpy as np
from scipy import ndimage
import sys
import json
import cv2
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

def get_frame_from_array(arr, width, height):
    frame_data = np.frombuffer(arr, dtype=np.uint8)
    frame_data = (frame_data.astype(np.float64)).reshape(height, width)
    return frame_data

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
    si_values = []
    chroma_si_u = []
    chroma_si_v = []
    ti_values = [0.0]
    previous_luma_data = None

    with open(filename, 'rb') as f:
        luma = f.read(frame_size)
        chroma_u = f.read(frame_size // 4)
        chroma_v = f.read(frame_size // 4)
        while len(luma) > 0:
            luma_data = get_frame_from_array(luma, width, height)
            chroma_u_data = get_frame_from_array(chroma_u, width // 2, height // 2)
            chroma_v_data = get_frame_from_array(chroma_v, width // 2, height // 2)
            cv2.imshow("Window", np.uint8(chroma_u_data))
            cv2.imshow("Window", np.uint8(chroma_v_data))
            si_values.append(calculate_si(luma_data))
            # add calculations for Chroma spatial information 
            chroma_si_u.append(calculate_si(chroma_u_data))
            chroma_si_v.append(calculate_si(chroma_v_data))
            if previous_luma_data is not None:
                ti_values.append(calculate_ti(luma_data, previous_luma_data))

            previous_luma_data = luma_data
            luma = f.read(frame_size)
            chroma_u = f.read(frame_size // 4)
            chroma_v = f.read(frame_size // 4)
    return si_values, chroma_si_u, chroma_si_v, ti_values



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python SI_TI_calculation.py filename")
    filename = sys.argv[1]
    width = 352
    height = 288
    si_orig, chU_orig, chV_orig, ti_orig = si_ti_calculation(filename, width, height)
    si_y = np.round(np.array(si_orig).astype(float), 3).tolist()
    si_u = np.round(np.array(chU_orig).astype(float), 3).tolist()
    si_v = np.round(np.array(chV_orig).astype(float), 3).tolist()
    ti = np.round(np.array(ti_orig).astype(float), 3).tolist()

    outfile = splitext(basename(filename))[0] + ".txt"
    with open(outfile, "w") as f:
        f.write("max_si_Y: {}\n".format(round(np.max(si_y), 3)))
        f.write("max_si_U: {}\n".format(round(np.max(si_u), 3)))
        f.write("max_si_V: {}\n".format(round(np.max(si_v), 3)))
        f.write("max_ti: {}\n".format(round(np.max(ti), 3)))
