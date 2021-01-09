from os.path import basename, splitext


def get_video_from_filename(filename):
    video_name = basename(filename)
    video_name = splitext(video_name)[0]
    video_name = video_name.split("_")[0]
    return video_name.title()


def get_int_from_line(line, token=":"):
    return float(line.split(token)[1].strip())


def parse_si_ti(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    si_Y = get_int_from_line(list(filter(lambda l: "si_Y" in l, lines))[0])
    si_U = get_int_from_line(list(filter(lambda l: "si_U" in l, lines))[0])
    si_V = get_int_from_line(list(filter(lambda l: "si_V" in l, lines))[0])
    ti = get_int_from_line(list(filter(lambda l: "ti" in l, lines))[0])
    return si_Y, si_U, si_V, ti

