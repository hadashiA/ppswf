import unittest
import os

from gif import GIF

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
gif_path = os.path.join(fixtures_dir, 'gogopher.gif')

class GIFParseTestCase(unittest.TestCase):
    def setUp(self):
        self.gif = GIF(open(gif_path))

    def testParseHeader(self):
        assert self.gif.signature == 'GIF'
        assert self.gif.width == 100
        assert self.gif.height == 100
        assert self.gif.global_color_table_flag
        assert self.gif.color_resolution == 8
        assert self.gif.sort_flag
