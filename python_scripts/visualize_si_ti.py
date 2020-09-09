from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange, std
import sys
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
    si = get_int_from_line(filter(lambda l: "si" in l, lines)[0])
    ti = get_int_from_line(filter(lambda l: "ti" in l, lines)[0])
    return si, ti


def visualize_data(videos, sis, tis):
    fig, ax = plt.subplots()
    ax.scatter(sis, tis)

    for i, txt in enumerate(videos):
            ax.annotate(txt, (sis[i], tis[i]))
    plt.xlabel("Spatial Information (SI)")
    plt.ylabel("Temporal Information (TI)")
    plt.savefig("videos_si_ti.png")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python visualize_si_ti.py input_dir")
        sys.exit(1)
    input_dir = sys.argv[1]
    files = []
    videos = []
    sis = []
    tis = []
    gops = [2, 4, 8, 16]
    files = glob('{}/*'.format(input_dir))

    for file_name in files:
        videos.append(get_video_from_filename(file_name))
        si, ti = parse_si_ti(file_name)
        sis.append(si)
        tis.append(ti)
    visualize_data(videos, sis, tis)
