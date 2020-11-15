from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange, std
import sys
from adjustText import adjust_text
import matplotlib


def get_video_from_filename(filename):
    video_name = basename(file_name)
    video_name = splitext(video_name)[0]
    video_name = video_name.split("_")[0]
    return video_name.title()


def get_int_from_line(line, token=":"):
    return float(line.split(token)[1].strip())


def parse_si_ti(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    si_Y = get_int_from_line(list(filter(lambda l: "si_Y" in l, lines))[0])
    si_U = get_int_from_line(list(filter(lambda l: "si_U" in l, lines))[0])
    si_V = get_int_from_line(list(filter(lambda l: "si_V" in l, lines))[0])
    ti = get_int_from_line(list(filter(lambda l: "ti" in l, lines))[0])
    return si_Y, si_U, si_V, ti


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
