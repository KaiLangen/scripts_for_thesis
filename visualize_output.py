import re
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt


def parseData(filename):
    with open(File, 'r') as f:
        data = f.readlines()
    data = [line.strip().split(',') for line in data]
    dataDict = {}
    # reorganize data such that all data from the same GOP are binned together
    for line in data:
        gopLevel = int(line[1])
        if gopLevel not in dataDict:
            dataDict[gopLevel] = []
        dataDict[gopLevel].append(line[2:])
    return dataDict

if __name__ == '__main__':       
    discoverFile = sys.argv[1]
    proposedFile = sys.argv[2]
    hasanFile = sys.argv[3]
    vidname = discoverFile.split('/')[1].split('.')[0]

    # read data and split
    discoverDict = parseData(discoverFile)
    proposedDict = parseData(proposedFile)
    hasanDict = parseData(hasanFile)

    for idx in range(1,5):
        plt.figure()
        gop = 2**idx
        x1,y1 = zip(*discoverDict[idx])
        plt.plot(x1, y1, '-o', label="Discover: GOP={}".format(gop), color='r')
        x2,y2 = zip(*proposedDict[idx])
        plt.plot(x2, y2, '-o', label="Proposed: GOP={}".format(gop), color='r')
        plt.legend(loc='lower right')
        #plt.savefig("{}_gop{}.png".format(vidname,gop))
        plt.show()
