from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
import sys
from adjustText import adjust_text
import matplotlib

from lib.si_ti_utils import *


def visualize_siti(videos, sis, tis):
    fig, ax = plt.subplots()
    ax.scatter(sis, tis)

    labels = [plt.text(sis[i], tis[i], videos[i], ha='center', va='center') for i in range(len(videos))]
    adjust_text(labels)
    plt.xlabel("Spatial Information (SI)")
    plt.ylabel("Temporal Information (TI)")
    plt.savefig("videos_si_ti.png")

def visualize_si_yuv(videos, sisY, sisU, sisV):
    fig, ax = plt.subplots()
    ax.scatter(sisY, sisU)
    ax.scatter(sisY, sisV)

    labels = [plt.text(sisY[i], sisU[i], videos[i], ha='center', va='center') for i in range(len(videos))]
    labels = [plt.text(sisY[i], sisV[i], videos[i], ha='center', va='center') for i in range(len(videos))]
    adjust_text(labels)
    plt.xlabel("Luma Spatial Information")
    plt.ylabel("Chroma Spatial Information")
    plt.savefig("videos_si_yuv.png")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python visualize_si_ti.py input_dir")
        sys.exit(1)
    input_dir = sys.argv[1]
    files = []
    videos = []
    sisY = []
    sisU = []
    sisV = []
    tis = []
    gops = [2, 4, 8, 16]
    files = glob('{}/*'.format(input_dir))

    for file_name in files:
        videos.append(get_video_from_filename(file_name))
        si_Y, si_U, si_V, ti = parse_si_ti(file_name)
        sisY.append(si_Y)
        sisU.append(si_U)
        sisV.append(si_V)
        tis.append(ti)
    visualize_siti(videos, sisY, tis)
    visualize_si_yuv(videos, sisY, sisU, sisV)
