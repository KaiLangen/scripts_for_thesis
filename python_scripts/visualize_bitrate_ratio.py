from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange, std, mean
import sys
import matplotlib


def parse_data_from_filedump(file_contents):
    file_data = {}
    for line in file_contents:
        if ":" in line:
            key, value =  line.strip().split(":")
            if key not in file_data:
                file_data[key] = []
            file_data[key].append(float(value))
    return file_data


def construct_data_set(files, video_names):
    data = {}
    for idx, file_name in enumerate(files):
        video = video_names[idx]
        with open(file_name, 'r') as f:
            data[video] = parse_data_from_filedump(f.readlines())
    return data


def get_stats(value):
    return value.mean(1), value.std(1)


def restructure_data(data, videos):
    lumas = []
    chromas = []
    others = []
    for video in videos:
        total = array(data[video]["average"])
        luma = array(data[video]["Coeffs. Y"]) / total
        chroma = array(data[video]["Coeffs. C"]) / total
        other = 1 - chroma - luma
        lumas.append(luma)
        chromas.append(chroma)
        others.append(other)
    return array(lumas), array(chromas), array(others)


def visualize_data(videos, lumas, chromas, others):
    width = 0.4
    ind = arange(len(lumas))
    luma_avg, luma_err = get_stats(lumas)
    chroma_avg, chroma_err = get_stats(chromas)
    other_avg, other_err = get_stats(others)
    p1 = plt.bar(ind, luma_avg, width=width, yerr=luma_err)
    p2 = plt.bar(ind, chroma_avg, width=width, bottom=luma_avg, yerr=chroma_err)
    p3 = plt.bar(ind, other_avg, width=width, bottom=luma_avg+chroma_avg, yerr=other_err)
    plt.legend((p1, p2, p3), ('Luma', 'Chroma', 'Other'), loc='lower right')
    plt.xticks(ind, videos)
    plt.show()


def parse_vid_names_from_filenames(filename):
    return ".".join(filename.split('.')[:-2])


def replace_id_with_canola(videos):
    for n, i in enumerate(videos):
        if i == "1507.2016.1108.images8":
            videos[n] = "canola"
    return videos


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print("Usage: python visualize_bitrate_ratio.py input_dir")
        sys.exit(1)

    input_dir = sys.argv[1]
    files = glob('{}/*.txt'.format(input_dir))
    fileNames = map(basename, files)
    videoNames = map(parse_vid_names_from_filenames, fileNames)
    videoNames = replace_id_with_canola(videoNames)
    videoNames = map(lambda x: x.title(), videoNames)
    data = construct_data_set(files, videoNames)
    lumas, chromas, others = restructure_data(data, videoNames)
    visualize_data(videoNames, lumas, chromas, others)
