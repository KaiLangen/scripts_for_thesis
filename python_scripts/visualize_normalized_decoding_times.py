from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange, std
import sys
import matplotlib 


fontsize = 18
linewidth = 3
markersize = 12
font = {'weight' : 'bold',
        'size'   : fontsize}

matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)
matplotlib.rc('font', **font)

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
    all_decoding_times = []
    for algo in colouring_algorithms:
        normalized_decoding_times = []
        for gop in gops:
            for video_name in videos:
                total_decoding_times = data[video_name][algo][gop][5, :]
                recoloured_frames = data[video_name][algo][gop][6, :]
                decoding_times_per_frame_ms = total_decoding_times / recoloured_frames * 1000
                normalized_decoding_times.extend(decoding_times_per_frame_ms)
        error = std(normalized_decoding_times)
        all_decoding_times.append(normalized_decoding_times)

    print([len(x) for x in all_decoding_times])
    plt.boxplot(all_decoding_times, labels=labels)
    plt.xlabel("Recolouring Algorithm")
    plt.ylabel("Decoding time (ms / Frame)")
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
