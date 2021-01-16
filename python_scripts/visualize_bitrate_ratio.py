from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import arange
import sys
import matplotlib.ticker as mtick

from lib.bitrate_utils import *



def visualize_data(videos, lumas, chromas, others):
    width = 0.4
    ind = arange(len(lumas))
    luma_avg, luma_err = get_stats(lumas)
    chroma_avg, chroma_err = get_stats(chromas)
    other_avg, other_err = get_stats(others)
    with open("bitrates.txt", "w") as f:
        for i in range(len(videos)):
            f.write("{}: {}\n".format(videos[i], chroma_avg[i]))
    fig, ax = plt.subplots()
    p1 = ax.bar(
        ind,
        other_avg,
       width=width,
        bottom=luma_avg+chroma_avg,
        yerr=other_err,
        color="#FEDAA7")
#        hatch="\\")
    p2 = ax.bar(ind,
        chroma_avg,
        width=width,
        bottom=luma_avg,
        yerr=chroma_err,
        color="#E85285")
#        hatch="x")
    p3 = ax.bar(ind,
        luma_avg,
        width=width,
        yerr=luma_err,
        color="#61169A")
#        hatch=".")
    ax.set_xlabel("Video Sequences")
    ax.set_ylabel("Percentage of Encoded Video")
    plt.legend((p1, p2, p3), ('Other', 'Chroma', 'Luma'), loc='lower right')
    plt.xticks(ind, videos)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.tight_layout()
    plt.savefig("bitrate_breakdown.png")


def wrap_vidname(video):
    splitstring = video.split('.')
    splitstring = ["%s %s" % (splitstring[2],splitstring[3]),
            "%s/%s/%s" % (splitstring[0][:2], splitstring[0][2:],splitstring[1])]
    return '\n'.join(splitstring)


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print("Usage: python visualize_bitrate_ratio.py input_dir")
        sys.exit(1)

    input_dir = sys.argv[1]
    files = glob('{}/*.txt'.format(input_dir))
    fileNames = map(basename, files)
    videoNames = map(parse_vid_name_from_filename, fileNames)
    videoNames = list(map(lambda x: x.title(), videoNames))
#    videoNames = list(map(lambda v: wrap_vidname(v), videoNames))
    data = construct_data_set(files, videoNames)
    lumas, chromas, others, _= restructure_data(data, videoNames)
    visualize_data(videoNames, lumas, chromas, others)
