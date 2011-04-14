import struct
import math
# import zlib
from cStringIO import StringIO

from bitstring import BitString

import swftag
from swftag import SWFTag
from utils import le2bytes, bytes2le

class SWFParseError(Exception):
    """Raised when fairue swf binary parse"""

class StructRect:
    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        first_byte = io.read(1)
        self.field_bits_length = ord(first_byte) >> 3
        bytes = first_byte + io.read(len(self) - 1)
        self.bits = BitString(bytes=bytes)

    def __getitem__(self, i):
        begin = 5 + i * self.field_bits_length
        end   = 5 + (i + 1) * self.field_bits_length
        return self.bits[begin:end].uint

    def __len__(self):
        total_bits_length = 5 + (self.field_bits_length * 4)
        return int(math.ceil(total_bits_length / 8.0))

    def build(self):
        return self.bits.bytes

class SWF:
    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        self.signature = io.read(3)
        self.version   = ord(io.read(1))
        self.filesize  = bytes2le(io.read(4))

        self.frame_size  = StructRect(io)
        self.frame_rate  = bytes2le(io.read(2)) / 0x100
        self.frame_count = bytes2le(io.read(2))

        # if self.is_compressed():
        #     body = io.read()
        #     io = StringIO(zlib.decompress(io.read()))
        #     self.signature = 'FWS'

        self.tags = []
        tag = None
        while tag is None or not isinstance(tag, swftag.End):
            tag = SWFTag(io)
            self.tags.append(tag)

    def is_compressed(self):
        if self.signature == 'CWS':
            return True
        elif self.signature == 'FWS':
            return False
        else:
            raise SWFParseError, 'invalid signature %s' % self.signature

    @property
    def x_min(self):
        return self.frame_size[0] / 20

    @property
    def x_max(self):
        return self.frame_size[1] / 20

    @property
    def y_min(self):
        return self.frame_size[2] / 20

    @property
    def y_max(self):
        return self.frame_size[3] / 20

    @property
    def width(self):
        return self.x_max - self.x_min

    @property
    def height(self):
        return self.y_max - self.y_min

    def build_header(self):
        return self.signature + \
               struct.pack('B', self.version) +  \
               le2bytes(self.filesize, 4) + \
               self.frame_size.build() + \
               le2bytes(self.frame_rate * 0x100, 2) + \
               le2bytes(self.frame_count, 2)
        
    def build(self):
        return self.build_header() + ''.join(tag.build() for tag in self.tags)

    def find_tag(self, cls):
        for tag in self.tags:
            if isinstance(tag, cls):
                return tag

    def find_tags(self, cls):
        return tuple(tag for tag in self.tags if isinstance(tag, cls))
