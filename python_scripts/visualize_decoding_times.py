from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange, std
import sys
import matplotlib 


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
    plt.figure()
    for grouping, algo in enumerate(colouring_algorithms):
        for idx, gop in enumerate(gops):
            decoding_times = []
            for video_name in videos:
                decoding_times.extend(data[video_name][algo][gop][5, :])
            error = std(decoding_times)
            x_pos = grouping*(len(gops) + 1) + idx
            plt.bar(
                x_pos,
                decoding_times,
                yerr=error,
                align='center',
                label="GOP {}".format(gop))
    plt.xlabel("Recolouring Algorithm")
    plt.ylabel("Decoding time (seconds)")
#    plt.xticks([x for x in x_pos)], labels)
    plt.legend()
    plt.show()


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
        #new_graph = '{}_gop{}.png'.format(video, gop)
        #plt.savefig(new_graph)
