import sys
from glob import glob
from os.path import basename

from lib.spatial_information import SpatialInformation
from lib.si_ti_utils import get_video_from_filename
from lib.bitrate_utils import \
    construct_data_set, \
    parse_vid_name_from_filename, \
    restructure_data


def get_true_percent_chroma_data(bitrate_dir):
    bitrate_files = glob('{}/*.txt'.format(bitrate_dir))
    videos = map(basename, bitrate_files)
    videos = list(map(parse_vid_name_from_filename, videos))
    bitrate_data = construct_data_set(bitrate_files, videos)
    lumas, chromas, others, qps = restructure_data(bitrate_data, videos)

    chroma_ratios = {}
    for i, video in enumerate(videos):
        chroma_ratios[video] = chromas[i]

    qp_by_video = {}
    for i, video in enumerate(videos):
        qp_by_video[video] = qps[i]
    return chroma_ratios, qp_by_video


def get_normalized_si_ratios(si_ti_dir):
    si_ti_files = glob('{}/*.txt'.format(si_ti_dir))
    si_data = {}
    for f in si_ti_files:
        video = get_video_from_filename(f)
        video = video.lower()
        si_info = SpatialInformation(f)
        si_data[video] = si_info.get_si_ratio()
    return si_data


def get_normalized_qp(qp):
    QP_MAX = 52
    return (QP_MAX - qp) / QP_MAX


def write_data_to_file(output_filename, percent_chroma_data, si_data, qp_data):
    with open(output_filename, 'w') as f:
        for k in percent_chroma_data.keys():
            for i in range(len(percent_chroma_data[k])):
                elements = [percent_chroma_data[k][i]]
                if qp_data:
                    elements.append(qp_data[k][i])
                elements.append(si_data[k])

                line = ", ".join([str(elem) for elem in elements])
                f.write(line + "\n")

