from glob import glob
from matplotlib import pyplot as plt
from os.path import basename
from numpy import array, stack
import sys

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



def get_video_from_filename(filename):
    basefile = basename(file_name)
    return '.'.join(basefile.split('.')[:-2])

def construct_data_set():
    data = {}
    for video in videos:
        data[video] = {}
        for algo in colouring_algorithms:
            file_name = "{}/{}.{}.dat".format(input_dir, video, algo)
            with open(file_name, 'r') as f:
                data[video][algo] = parse_data_from_filedump(f.readlines())
    return data


def visualize_data(video_name, gop, axis):
    print(video_name, gop)
    video_data = data[video_name]
    data_subset = []
    for algo in colouring_algorithms:
        data_subset.append(video_data[algo][gop])
    stacked = stack(data_subset, 2)
    bitrate = stacked[1, :, :]
    psnr = stacked[2, :, :]
    orig_bitrate = stacked[3, :, 0]
    orig_psnr = stacked[4, :, 0]
    for idx, algo in enumerate(colouring_algorithms):
        axis.plot(bitrate[:, idx], psnr[:, idx], label=labels[idx])
    axis.plot(orig_bitrate, orig_psnr, label='Intra')
    axis.plot(bitrate[:, 0], orig_psnr, label='Theoretical Max')
    plt.legend()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage python new_parse.py dir")
        sys.exit(1)
    input_dir = sys.argv[1]
    colouring_algorithms = ['hasan', 'proposed', 'discover']
    labels = ['Hasan', 'MCR', 'MCI']
    files = {}
    videos = []
    gops = [2, 4, 8, 16]
    for algo in colouring_algorithms:
        files[algo] = glob('{}/*{}.dat'.format(input_dir, algo))

    for file_name in files[algo]:
        videos.append(get_video_from_filename(file_name))

    data = construct_data_set()

    for video in videos:
        fig, axes = plt.subplots(1, len(gops) - 1)
        fig.subplots_adjust(wspace=0)
        for idx, gop in enumerate(gops[1:]):
            visualize_data(video, gop, axes[idx])
        plt.show()
