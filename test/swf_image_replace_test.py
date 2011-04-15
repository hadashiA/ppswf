import os
import unittest

from bitstring import BitString

from ppswf import SWF, swftag
from ppswf.jpeg import JPEG

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
swf_path  = os.path.join(fixtures_dir, 'orz.swf')
jpeg_path = os.path.join(fixtures_dir, 'gogopher.jpg')

class JPEGReplaceTestCase(unittest.TestCase):
    def setUp(self):
        self.swf = SWF(open(swf_path).read())
        self.jpeg_tag = self.swf.find_tag(swftag.DefineBitsJPEG2)

    def testUpdateFileSize(self):
        assert True
