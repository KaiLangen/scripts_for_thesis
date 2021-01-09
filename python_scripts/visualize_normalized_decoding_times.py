from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange, std, mean
import sys
import matplotlib 

def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

def parse_data_from_filedump(file_dump):
    file_data = {}
    for line in file_dump:
        line_data = line.strip().split(',')
        gop = int(line_data[0])
        tup = array([float(x) for x in line_data[1:]], dtype='float')
        if sum(tup) == 0:
            continue
        if gop not in file_data:
            file_data[gop] = []
        file_data[gop].append(tup)
    for gop in gops:
        file_data[gop] = stack(file_data[gop], 1)
    return file_data



def get_video_from_filename(filename, colouring_algorithms):
    video_name = basename(file_name)
    video_name = splitext(video_name)[0]
    for algo in colouring_algorithms:
        video_name = video_name.replace(algo, '')
    video_name = video_name[:-1]
    return video_name


def construct_data_set():
    data = {}
    for video in videos:
        data[video] = {}
        for algo in colouring_algorithms:
            file_name = "{}/{}.{}.dat".format(input_dir, video, algo)
            with open(file_name, 'r') as f:
                data[video][algo] = parse_data_from_filedump(f.readlines())
    return data


def visualize_data(videos, gops):
    group_size = len(colouring_algorithms)
    fig, ax = plt.subplots()
    for idx, algo in enumerate(colouring_algorithms):
        normalized_decoding_times = []
        for gop in gops:
            for video_name in videos:
                total_decoding_times = data[video_name][algo][gop][5, :]
                recoloured_frames = data[video_name][algo][gop][6, :]
                decoding_times_per_frame_ms = total_decoding_times / recoloured_frames * 1000
                normalized_decoding_times.extend(decoding_times_per_frame_ms)
        error = std(normalized_decoding_times)
        bar = ax.bar(idx, mean(normalized_decoding_times), yerr=error)
        autolabel(ax, bar)
    ax.set_xlabel("Recolouring Algorithm")
    ax.set_ylabel("Decoding time (ms / Frame)")
    ax.set_ylim(0, 1200)
    plt.xticks(range(len(labels)), labels)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    input_dir = sys.argv[1]
    colouring_algorithms = ['hasan', 'discover', 'proposed', 'mcr.fast']
    labels = ['Hasan', 'MCI', 'MCR', 'MCR Fast']
    markers = ['X', 'D', 'v', 's', 'P', 'o']
    line_style = ['-', '-.', ':', '--']
    files = {}
    videos = []
    gops = [2, 4, 8, 16]
    for algo in colouring_algorithms:
        files[algo] = glob('{}/*.{}.dat'.format(input_dir, algo))

    for file_name in files[algo]:
        videos.append(get_video_from_filename(file_name, colouring_algorithms))

    data = construct_data_set()

    visualize_data(videos, gops)
    new_graph = 'decoding_times.png'
    plt.savefig(new_graph)
