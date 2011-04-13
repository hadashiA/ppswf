import unittest
import os
import sys



from ppswf import SWF, SWFTag, StructRect

fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
cws_path = os.path.join(fixtures_dir, 'orz.swf')
cws_bytes = open(cws_path).read()
# [HEADER]        File version: 4
# [HEADER]        File size: 7031
# [HEADER]        Frame rate: 10.000000
# [HEADER]        Frame count: 40
# [HEADER]        Movie width: 240.00
# [HEADER]        Movie height: 240.00

class StructRectTestCase(unittest.TestCase):
    def setUp(self):
        self.rect = StructRect(cws_bytes[8:])
        self.original_bytes = cws_bytes[8:8+len(self.rect)]

    def testParseRect(self):
        assert self.rect[0] == 0
        assert self.rect[1] == 4800
        assert self.rect[2] == 0
        assert self.rect[3] == 4800

    def testBuildRect(self):
        assert self.rect.build() == self.original_bytes

class SWFTagTestCase(unittest.TestCase):
    def setUp(self):
        self.swf = SWF(cws_bytes)
        self.tag_short = self.swf.tags[0]
        self.tag_long  = self.swf.tags[1]

        tag_short_start = self.swf.header_bytes_length
        tag_short_end   = tag_short_start + len(self.tag_short)
        self.tag_short_original_bytes = cws_bytes[tag_short_start:tag_short_end]

        tag_long_start = tag_short_end
        tag_long_end   = tag_long_start + len(self.tag_long)
        self.tag_long_original_bytes = cws_bytes[tag_long_start:tag_long_end]

    def testParseTagShort(self):
        assert self.tag_short.type_name() == 'SetBackgoundColor'
        assert self.tag_short.body_bytes_length == 3
        assert len(self.tag_short.body_bytes) == self.tag_short.body_bytes_length
        assert self.tag_short.body_bytes[0] == '\xff'
        assert self.tag_short.body_bytes[1] == '\xff'
        assert self.tag_short.body_bytes[2] == '\xff'

    def testParseTagLong(self):
        assert self.tag_long.type_name() == 'DefineBitsJPEG2'
        assert self.tag_long.body_bytes_length == 2276
        assert len(self.tag_long.body_bytes) == self.tag_long.body_bytes_length

class SWFTestCase(unittest.TestCase):
    def setUp(self):
        self.swf = SWF(cws_bytes)
        
    def testParseHeader(self):
        assert self.swf.signature == 'FWS'
        assert not self.swf.is_compressed()
        assert self.swf.version == 4
        assert self.swf.filesize == 7031
        assert self.swf.x_min == 0
        assert self.swf.x_max == 240
        assert self.swf.y_min == 0
        assert self.swf.y_max == 240
        assert self.swf.frame_rate == 10.0
        assert self.swf.frame_count == 40

if __name__ == '__main__':
    unittest.main()
