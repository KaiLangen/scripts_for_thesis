from glob import glob
from matplotlib import pyplot as plt
from matplotlib import gridspec
from os.path import basename
from numpy import array, stack, arange
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

    print("")
    print("")
    print(video_name, gop)
    print("bitrate", orig_bitrate, bitrate)
    print("psnr", orig_psnr, psnr)
    plt.plot(
        orig_bitrate,
        orig_psnr,
        label='Intra',
        marker=markers[-2],
        fillstyle='none',
            linewidth=linewidth,
        markersize=markersize)
    plt.plot(bitrate[:, 0],
            orig_psnr,
            label='Theoretical Max',
            marker=markers[-1],
            linewidth=linewidth,
            markersize=markersize)
    plt.title('GOP={}'.format(gop))
    for idx, algo in enumerate(colouring_algorithms):
        plt.plot(
            bitrate[:, idx],
            psnr[:, idx],
            label=labels[idx],
            marker=markers[idx],
            linestyle=line_style[idx],
            linewidth=linewidth,
            markersize=markersize)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage python new_parse.py dir")
        sys.exit(1)
    input_dir = sys.argv[1]
    colouring_algorithms = ['hasan', 'discover', 'proposed']
    labels = ['Hasan', 'MCI', 'MCR']
    markers = ['X', 'D', 'v', 's', 'P']
    line_style = ['--', '-.', ':']
    files = {}
    videos = []
    gops = [2, 4, 8, 16]
    for algo in colouring_algorithms:
        files[algo] = glob('{}/*{}.dat'.format(input_dir, algo))

    for file_name in files[algo]:
        videos.append(get_video_from_filename(file_name))

    data = construct_data_set()

    for video in videos:
        for idx, gop in enumerate(gops):
            plt.figure()
            visualize_data(video, gop)
            plt.ylabel("Average PSNR")
            plt.xlabel("Average mB / s")
            plt.legend(loc='lower right')
            plt.savefig('{}_{}.png'.format(video, gop))
