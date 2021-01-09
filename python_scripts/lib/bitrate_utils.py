from numpy import array, std, mean


def parse_data_from_filedump(file_contents):
    file_data = {}
    for line in file_contents:
        if ":" in line:
            key, value =  line.strip().split(":")
            if key not in file_data:
                file_data[key] = []
            file_data[key].append(float(value))
    return file_data


def construct_data_set(files, video_names):
    data = {}
    for idx, file_name in enumerate(files):
        video = video_names[idx]
        with open(file_name, 'r') as f:
            data[video] = parse_data_from_filedump(f.readlines())
    return data


def get_stats(value):
    return value.mean(1), value.std(1)


def restructure_data(data, videos):
    lumas = []
    chromas = []
    others = []
    for video in videos:
        total = array(data[video]["average"])
        luma = array(data[video]["Coeffs. Y"]) / total * 100
        chroma = array(data[video]["Coeffs. C"]) / total * 100
        other = 100 - chroma - luma
        lumas.append(luma)
        chromas.append(chroma)
        others.append(other)
    return array(lumas), array(chromas), array(others)


def parse_vid_name_from_filename(filename):
    return ".".join(filename.split('.')[:-2])

