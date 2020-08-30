from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename, splitext
from numpy import array, stack, arange
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


def visualize_data(video_name, gop):
    video_data = data[video_name]
    data_subset = []
    for algo in colouring_algorithms:
        data_subset.append(video_data[algo][gop])
    stacked = stack(data_subset, 2)
    bitrate = stacked[1, :, :] / 1000
    psnr = stacked[2, :, :]
    orig_bitrate = stacked[3, :, 0] / 1000
    orig_psnr = stacked[4, :, 0]

    plt.plot(bitrate[:, 0],
            orig_psnr,
            label='Theoretical Max',
            marker=markers[-1])
    plt.title('GOP={}'.format(gop))
    for idx, algo in enumerate(colouring_algorithms):
        plt.plot(
            bitrate[:, idx],
            psnr[:, idx],
            label=labels[idx],
            marker=markers[idx],
            linestyle=line_style[idx])
    plt.plot(
        orig_bitrate,
        orig_psnr,
        label='Intra',
        marker=markers[0],
        fillstyle='none')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage python new_parse.py dir")
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
        files[algo] = glob('{}/*{}.dat'.format(input_dir, algo))

    for file_name in files[algo]:
        videos.append(get_video_from_filename(file_name, colouring_algorithms))

    data = construct_data_set()

    for video in videos:
        for idx, gop in enumerate(gops):
            plt.figure()
            visualize_data(video, gop)
            plt.ylabel("Average PSNR")
            plt.xlabel("Average mB / s")
            plt.legend(loc='lower right')
            new_graph = '{}_gop{}.png'.format(video, gop)
            print(new_graph)
            plt.savefig(new_graph)
