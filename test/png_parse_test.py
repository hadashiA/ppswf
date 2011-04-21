import unittest
import os
import struct

from bitstring import BitString

from png import PNG

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
png_path = os.path.join(fixtures_dir, 'gogopher.png')

class PNGParseTestCase(unittest.TestCase):
    def setUp(self):
        self.png = PNG(open(png_path))

    def testParseIHDR(self):
        assert self.png.width == 100
        assert self.png.height == 100
        assert self.png.depth == 8
