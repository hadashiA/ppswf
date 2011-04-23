import unittest
import os
import struct

from bitstring import BitString

from utils import rgb
from gif import GIF

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
# gif_path = os.path.join(fixtures_dir, 'gogopher.gif')
gif_path = os.path.join(fixtures_dir, 'sample.gif')

# Version: GIF89a
# Logical screen width: 120
# Logical screen height: 180
# Flags: [True, True, True, False, True, True, True, True]
#        Color resolution: 7
#        Sort flag: False
#        Global color table flag: True
#                        ...size: 256 (768 bytes)
# Background color: 0
# Aspect ratio info: 0

class GIFParseTestCase(unittest.TestCase):
    def setUp(self):
        self.gif = GIF(open(gif_path))

    def testParseHeader(self):
        assert self.gif.signature == 'GIF'
        assert self.gif.width == 120
        assert self.gif.height == 180
        assert self.gif.pallete_flag
        assert self.gif.color_resolution == 8
        assert self.gif.sort_flag
        assert self.gif.pallete_size == 256

    def testParseImageBlock(self):
        image_block = self.gif.blocks[1]
        assert image_block.left_pos == 0
        assert image_block.top_pos == 0
        assert image_block.width == 120
        assert image_block.height == 180
        assert not image_block.pallete_flag

    def testParseColorPallete(self):
        image_block = self.gif.images[0]
        assert rgb(image_block.pallete_bytes) == (
            ( 43, 80,121),
            ( 68, 68, 68),
            ( 75, 75, 75),
            ( 83, 83, 83),
            ( 89, 89, 89),
            ( 65, 85,127),
            ( 98, 98, 98),
            (107,107,107),
            (116,116,116),
            (125,125,125),
            (142,117,117),
            ( 90,148,119),
            ( 55, 93,149),
            ( 54,100,147),
            ( 50,108,167),
            ( 80,109,159),
            ( 71,110,173),
            ( 86,119,186),
            ( 61, 61,220),
            ( 61, 61,228),
            ( 60, 60,237),
            ( 58, 58,244),
            ( 53, 53,251),
            ( 60, 60,251),
            ( 64, 63,233),
            ( 58, 73,247),
            ( 59,118,236),
            ( 81, 81,203),
            ( 76, 76,211),
            ( 83, 83,212),
            ( 89, 89,216),
            ( 82,122,203),
            (112,109,209),
            (120,120,217),
            ( 68, 67,235),
            ( 89, 89,232),
            ( 65, 65,244),
            ( 67, 67,251),
            ( 75, 75,250),
            ( 76, 85,249),
            ( 88, 89,245),
            ( 84, 84,249),
            ( 92, 92,249),
            ( 98, 95,239),
            ( 89, 98,248),
            ( 82,118,247),
            (100,100,233),
            (107,115,235),
            (124,124,227),
            (124,125,234),
            (104,106,245),
            (100,100,249),
            (108,108,250),
            (113,111,248),
            (101,118,249),
            (116,115,250),
            (117,119,248),
            (123,123,249),
            (131,124,203),
            (134,120,234),
            (111,147,142),
            ( 96,145,151),
            (107,155,147),
            (107,164,154),
            (118,166,154),
            (112,178,145),
            ( 83,133,185),
            (121,177,169),
            (122,180,170),
            (125,201,163),
            ( 47,128,211),
            ( 52,134,216),
            ( 56,137,235),
            ( 86,140,207),
            (106,148,209),
            (118,166,217),
            (115,178,215),
            ( 82,147,234),
            (105,153,252),
            (114,146,243),
            ( 88,164,241),
            (112,172,240),
            (121,165,253),
            (130,130,130),
            (138,138,138),
            (142,142,142),
            (147,147,147),
            (155,155,155),
            (174,146,146),
            (138,175,160),
            (132,184,172),
            (134,188,179),
            (148,177,177),
            (164,164,164),
            (172,172,172),
            (174,177,178),
            (177,177,177),
            (186,186,186),
            (204,173,174),
            (215,183,184),
            (226,188,188),
            (133,197,186),
            (141,196,187),
            (146,202,181),
            (162,204,183),
            (236,212,189),
            (133,132,218),
            (147,149,211),
            (171,152,215),
            (144,175,217),
            (175,176,213),
            (132,132,228),
            (138,138,228),
            (132,131,237),
            (139,139,237),
            (144,142,235),
            (150,148,234),
            (132,131,244),
            (139,140,244),
            (131,131,249),
            (139,139,249),
            (136,149,247),
            (147,148,245),
            (148,148,251),
            (156,156,250),
            (162,158,245),
            (141,176,232),
            (134,170,251),
            (150,167,248),
            (136,184,248),
            (152,184,250),
            (175,176,230),
            (164,163,249),
            (164,170,249),
            (171,171,249),
            (165,182,247),
            (180,180,251),
            (187,187,250),
            (211,183,204),
            (196,186,239),
            (139,203,206),
            (152,203,197),
            (133,215,202),
            (153,212,202),
            (138,216,212),
            (150,220,212),
            (167,200,199),
            (165,214,203),
            (177,203,210),
            (169,217,214),
            (183,217,215),
            (141,226,211),
            (148,226,213),
            (154,231,219),
            (178,228,202),
            (166,230,219),
            (162,234,222),
            (183,229,219),
            (147,204,230),
            (139,195,251),
            (151,197,251),
            (154,204,255),
            (169,200,233),
            (176,206,234),
            (185,216,232),
            (167,201,251),
            (180,203,252),
            (168,212,252),
            (183,216,252),
            (152,234,228),
            (165,235,228),
            (172,237,226),
            (179,237,227),
            (186,233,229),
            (169,243,231),
            (182,245,235),
            (188,243,234),
            (168,234,243),
            (182,233,245),
            (184,248,243),
            (189,253,243),
            (195,195,195),
            (196,200,205),
            (203,203,203),
            (217,210,203),
            (208,204,211),
            (211,211,211),
            (217,213,217),
            (220,220,220),
            (230,199,200),
            (236,214,196),
            (239,216,193),
            (232,218,204),
            (242,220,197),
            (245,222,201),
            (230,201,211),
            (234,214,214),
            (244,217,218),
            (199,234,219),
            (213,225,223),
            (246,227,205),
            (239,227,217),
            (244,228,212),
            (248,231,209),
            (248,233,213),
            (243,231,219),
            (249,235,219),
            (199,199,231),
            (208,211,231),
            (195,195,249),
            (201,204,249),
            (198,215,250),
            (195,219,253),
            (203,220,253),
            (218,218,249),
            (233,217,230),
            (245,220,227),
            (199,234,231),
            (213,233,233),
            (195,245,236),
            (203,244,237),
            (195,249,239),
            (215,243,236),
            (200,230,251),
            (210,227,254),
            (211,234,254),
            (217,234,250),
            (203,245,245),
            (196,252,243),
            (204,253,245),
            (215,244,246),
            (211,253,246),
            (218,251,245),
            (212,254,248),
            (220,254,249),
            (227,227,227),
            (234,229,231),
            (237,237,237),
            (253,228,229),
            (245,232,229),
            (250,238,227),
            (254,235,235),
            (250,240,230),
            (250,241,234),
            (230,232,250),
            (241,238,241),
            (231,246,250),
            (228,253,252),
            (235,253,253),
            (244,244,244),
            (253,244,242),
            (251,249,246),
            (242,244,253),
            (243,252,253),
            (255,255,254),
            (  0,  0,  0))
        

class GIFOneColorParseTestCase(unittest.TestCase):
    def setUp(self):
        red_path = os.path.join(fixtures_dir, 'red.gif')
        self.gif = GIF(open(red_path))
        

    def testParseOneColor(self):
        assert len(self.gif.images) == 1
        assert self.gif.width == 40
        assert self.gif.height == 40

        image_block = self.gif.images[0]
        assert image_block.width == 40
        assert image_block.height == 40
        print rgb(image_block.pallete_bytes)
        assert rgb(image_block.pallete_bytes) == (
            (255, 0, 0),
            (0, 0, 0)
            )
        
    def testParseLZW(self):
        image_block = self.gif.images[0]
        bytes = image_block.build_indices()
        l = struct.unpack('%dB' % len(bytes), bytes)
        assert list(set(l)) == [0]

class GifGogopherParseTestCase(unittest.TestCase):
    def setUp(self):
        gif_path = os.path.join(fixtures_dir, 'gogopher.gif')
        self.gif = GIF(open(gif_path))
        self.image_block = self.gif.images[0]

    def testParseHeader(self):
        assert self.gif.version == '89a'
        assert self.gif.width == 100
        assert self.gif.height == 100
        assert self.gif.bgcolor_index == 0
        assert self.gif.aspect_ratio == 0

    # def testParseImageBlock(self):
    #     assert self.image_block.left_pos == 0
    #     assert self.image_block.top_pos == 0
    #     assert self.image_block.width == 100
    #     assert self.image_block.height == 100
    #     assert not self.image_block.pallete_flag
    #     assert self.image_block.lzw_min_code_size == 7
