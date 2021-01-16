from lib.si_ti_utils import parse_si_ti

class SpatialInformation:
    def __init__(self, file_name):
        si_Y, si_U, si_V, _ = parse_si_ti(file_name)
        self.luma_information = si_Y 
        self.chroma_u_information = si_U
        self.chroma_v_information = si_V

    def get_si_ratio(self):
        return ((self.chroma_u_information + self.chroma_v_information) / self.luma_information)
