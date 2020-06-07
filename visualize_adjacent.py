import re
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt


def parse_data():
    pass

def visualize_graph():
    pass

if __name__ == '__main__':       
    if len(sys.argv) != 3:
        print("Usage: python visualize_adjacent.py dir")
        sys.exit()
    input_dir = sys.argv[1]

    # read data and split
    with open(discoverFile, 'r') as f:
        discoverData = f.readlines()
    discoverData = [line.strip().split(',') for line in discoverData]
    discoverDict = {}
    # reorganize data such that all data from the same GOP are binned together
    for line in discoverData:
        gopLevel = int(line[1])
        tup = [float(x) for x in line[2:]]
        if sum(tup) == 0:
            continue
        if gopLevel not in discoverDict:
            discoverDict[gopLevel] = []
        discoverDict[gopLevel].append(tup)

    # repeat the same process for proposed codec data
    with open(proposedFile, 'r') as f:
        proposedData = f.readlines()
    proposedData = [line.strip().split(',') for line in proposedData]
    proposedDict = {}
    for line in proposedData:
        gopLevel = int(line[1])
        tup = [float(x) for x in line[2:]]
        if sum(tup) == 0:
            continue
        if not gopLevel in proposedDict:
            proposedDict[gopLevel] = []
        proposedDict[gopLevel].append(tup)

    for idx in range(2,5):
        gop = 2**idx
        plt.figure()
        x0,y0 = zip(*discoverDict[1])
        x1,y1 = zip(*discoverDict[idx])
        x2,y2 = zip(*proposedDict[idx])
        plt.plot(x0, y0, '-o', label="Discover: GOP=2", color='g')
        plt.plot(x1, y1, '-o', label="Discover: GOP={}".format(gop), color='r')
        plt.plot(x2, y2, '-o', label="Proposed: GOP={}".format(gop), color='b')
        plt.title("Rate Distortion Comparison")
        plt.xlabel("Average kB / frame")
        plt.ylabel("Average PSNR")
        plt.legend(loc='lower right')
        plt.show()
