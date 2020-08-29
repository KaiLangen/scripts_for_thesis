from __future__ import print_function

import re
import numpy as np
import sys
from os.path import join, exists

def parseChromaStats(filename, key):
    with open(filename, 'r') as f:
        lines = f.readlines()
    frameOrder =[]
    psnr =[]
    for line in lines:
        m = re.search('(?<=Decoding frame )\d+', line)
        if m:
            frameOrder.append(int(m.group(0)))
        m = re.search('(?<={} )[0-9.]+'.format(key), line)
        if m:
            psnr.append(float(m.group(0)))

    return frameOrder, psnr

def parseDecTime(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        m = re.search('(?<=real)\s+\d+m\d+\.\d+', line)
        if m:
            m = m.group(0).lstrip('\s')
            time = [float(x) for x in m.split('m')]
            return time[0]*60.0 + time[1]
    return None


def parseIntraStats(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    avgPSNRY = 0
    avgPSNRU = 0
    avgPSNRV = 0
    avgBits = 0
    avgChromaBits = 0
    nFrames = 0
    for line in lines:
        m = re.search('(?<=SNR Y\(dB\))[ |]+[0-9.]+', line)
        if m:
            avgPSNRY = float(m.group(0).lstrip(' |'))
            continue
        m = re.search('(?<=SNR U\(dB\))[ |]+[0-9.]+', line)
        if m:
            avgPSNRU = float(m.group(0).lstrip(' |'))
            continue
        m = re.search('(?<=SNR V\(dB\))[ |]+[0-9.]+', line)
        if m:
            avgPSNRV = float(m.group(0).lstrip(' |'))
            continue

        m = re.search('(?<=average bits/frame)[ |]+[0-9.]+', line)
        if m:
            avgBits = float(m.group(0).lstrip(' |'))
            continue
        m = re.search('(?<=Coeffs. C)[ |]+[0-9.]+', line)
        if m:
            avgChromaBits = float(m.group(0).lstrip(' |'))
            continue
	m = re.search('(?<=No.of coded pictures)[ :]+[0-9]+', line)
        if m:
            nFrames = int(m.group(0).lstrip(' :'))

    return (30*(avgBits-avgChromaBits)/1000.0,
            avgPSNRY, 
            30*avgBits/1000.0,
            (6*avgPSNRY+avgPSNRU+avgPSNRV)/8,
            nFrames)


def parseKeyChromaStats(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    avgPSNRU = 0
    avgPSNRV = 0
    avgChromaBits = 0
    nFrames = 0
    for line in lines:
        m = re.search('(?<=SNR Y\(dB\))[ |]+[0-9.]+', line)
        if m:
            avgPSNRY = float(m.group(0).lstrip(' |'))
            continue
        m = re.search('(?<=SNR U\(dB\))[ |]+[0-9.]+', line)
        if m:
            avgPSNRU = float(m.group(0).lstrip(' |'))
            continue
        m = re.search('(?<=SNR V\(dB\))[ |]+[0-9.]+', line)
        if m:
            avgPSNRV = float(m.group(0).lstrip(' |'))
            continue
        m = re.search('(?<=Coeffs. C)[ |]+[0-9.]+', line)
        if m:
            avgChromaBits = float(m.group(0).lstrip(' |'))
            continue
	m = re.search('(?<=No.of coded pictures)[ :]+[0-9]+', line)
        if m:
            nFrames = int(m.group(0).lstrip(' :'))

        avgPSNR = (avgPSNRU + avgPSNRV) / 2.0
    return (30*avgChromaBits/1000.0, avgPSNR, nFrames)

###############################################################################

if __name__ == '__main__':       
    if len(sys.argv) != 4:
        print("Usage: python parse_output.py dataDir codecType qpLevel")
        sys.exit()
    dataDir = sys.argv[1]
    codecType = sys.argv[2]
    qpLevel = int(sys.argv[3])
    if not exists(dataDir):
        print("Error: invalid directory path: {}".format(dataDir))
        sys.exit()

    keyQP = [x for x in range(22,36,2)]
    rate = []
    psnr = []
    for i in range(1,5):
        gop = (1 << i)
        # file names
        keyFile = join(dataDir,"stats_{}_{}.dat".format(keyQP[qpLevel],i))
        oracleFile = join(dataDir,"stats_{}.dat".format(keyQP[qpLevel]))
        wzFile = join(dataDir,"{}/dec_{}_{}.log".format(codecType,keyQP[qpLevel],i))
        timeFile = join(dataDir,"{}/dec_time_{}_{}.log".format(codecType,keyQP[qpLevel],i))

	# parse files, collect raw data
        key_chroma_kbps, key_chroma_psnr, nKeys = parseKeyChromaStats(keyFile)
        luma_kbps, luma_psnr, orig_kbps, orig_psnr, _ = parseIntraStats(oracleFile)
        decTime = parseDecTime(timeFile)

        if codecType == "proposed":
            frameOrder,ChromaPsnrU = parseChromaStats(wzFile,"PSNR Recoloured Chroma \(U\):")
            frameOrder,ChromaPsnrV = parseChromaStats(wzFile,"PSNR Recoloured Chroma \(V\):")
        elif codecType == "discover":
            wzFileU = join(dataDir,"discover/dec_{}_{}_u.log".format(keyQP[qpLevel],i))
            frameOrder,ChromaPsnrU = parseChromaStats(wzFileU, "PSNR Recoloured Chroma:")
            wzFileV = join(dataDir,"discover/dec_{}_{}_v.log".format(keyQP[qpLevel],i))
            frameOrder,ChromaPsnrV = parseChromaStats(wzFileV, "PSNR Recoloured Chroma:")
        elif codecType == "hasan":
            frameOrder,ChromaPsnrU = parseChromaStats(wzFile,"PSNR Recoloured Chroma \(U\):")
            frameOrder,ChromaPsnrV = parseChromaStats(wzFile,"PSNR Recoloured Chroma \(V\):")
        else:
            raise ValueError("Invalid codecType: {}".format(codecType))

        if not exists(keyFile):
            raise ValueError('Error: file {} does not exist'.format(keyFile))
        nChromaFrames = len(frameOrder)
        chromaPsnr = sum(ChromaPsnrU + ChromaPsnrV)/(2*nChromaFrames)
#        print(nChromaFrames, chromaPsnr, file=sys.stderr)

	nFrames = nKeys + nChromaFrames
        rate.append(luma_kbps + key_chroma_kbps*nKeys/nFrames)
	weightedChromaPsnr = (chromaPsnr*nChromaFrames + key_chroma_psnr*nKeys) / nFrames
	psnr.append((6*luma_psnr + 2*weightedChromaPsnr)/8)
        print("{},{},{},{},{},{},{}".format(gop, keyQP[qpLevel], 
                                         rate[-1], psnr[-1],
                                         orig_kbps, orig_psnr, decTime))
   
