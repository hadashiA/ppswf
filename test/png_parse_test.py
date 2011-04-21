import unittest
import os
import struct

from bitstring import BitString

import utils
from png import PNG

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')

class PNGColorType3ParseTestCase(unittest.TestCase):
    def setUp(self):
        png_path = os.path.join(fixtures_dir, 'gogopher.png')
        self.png = PNG(open(png_path))

    def testParseIHDR(self):
        assert self.png.width == 100
        assert self.png.height == 100
        assert self.png.depth == 8
        assert self.png.color_type == 3

    def testParsePLTE(self):
        assert utils.rgb(self.png.pallete_bytes) == (
            (  0,  0,  1),
            (  4,  4, 10),
            ( 26, 26, 28),
            ( 32, 31, 37),
            ( 16, 15, 20),
            (  6,  4, 16),
            ( 86, 86, 90),
            (157,157,162),
            (206,206,209),
            (197,197,201),
            (191,192,196),
            (179,179,180),
            (186,186,188),
            (195,195,195),
            ( 91, 91, 92),
            ( 21, 21, 25),
            ( 40, 39, 44),
            ( 56, 55, 62),
            ( 23, 21, 32),
            (  7,  8, 11),
            ( 62, 64, 63),
            (123,123,124),
            (239,240,243),
            (254,254,254),
            (223,224,226),
            (104,103,108),
            ( 80, 79, 84),
            ( 76, 76, 77),
            ( 43, 43, 44),
            ( 63, 63, 65),
            (227,227,229),
            (176,175,181),
            (102,101,105),
            (230,230,234),
            (246,246,249),
            (223,222,226),
            (151,150,155),
            ( 35, 35, 37),
            ( 93, 91,105),
            (248,247,252),
            (117,117,122),
            (216,215,220),
            (249,249,247),
            (246,248,247),
            (211,211,212),
            (131,131,132),
            (108,109,113),
            (166,166,169),
            (107,107,108),
            (236,236,237),
            (125,125,130),
            ( 59, 59, 60),
            (219,219,220),
            ( 45, 45, 49),
            ( 88, 87, 92),
            ( 99, 99,100),
            (204,204,204),
            ( 79, 80, 84),
            (167,168,170),
            (147,147,148),
            ( 10, 10, 13),
            (103,105,104),
            (189,189,194),
            (171,172,172),
            ( 68, 68, 69),
            (140,140,140),
            (163,162,164),
            (115,115,116),
            (155,155,156),
            ( 81, 81, 79),
            (  8,  7, 12),
            (212,212,217),
            (136,136,134),
            (184,184,182),
            ( 72, 72, 70),
            (238,237,242),
            ( 19, 19, 21),
            (166,164,177),
            ( 77, 76, 83),
            ( 69, 69, 73),
            (132,131,136),
            ( 92, 92, 97),
            (182,181,186),
            ( 29, 28, 33),
            (136,135,140),
            (174,174,177),
            (244,244,245),
            ( 50, 50, 51),
            (143,144,146),
            (142,141,147),
            (208,207,212),
            (240,239,244),
            ( 83, 83, 84),
            ( 35, 35, 41),
            (161,159,170),
            (152,151,157),
            ( 13, 11, 25),
            ( 53, 52, 58),
            (199,197,208),
            )

    def testXRGBBytes(self):
        d = {}
        # for xrgb in utils.rgba(self.png.build_xrgb()):
        #     if not d.has_key(xrgb):
        #         d[xrgb] = 0
        #     d[xrgb] += 1
        pallete = utils.rgb(self.png.pallete_bytes)
        for index in map(ord, self.png.indices_bytes):
            rgb = pallete[index]
            if not d.has_key(rgb):
                d[rgb] = 0
            d[rgb] += 1

        for k, v in sorted(d.items(), cmp=lambda a,b:cmp(b,a), key=lambda x:x[1]):
            print str(k).rjust(11), v
        # print len(self.png.indices_bytes)

        assert False
