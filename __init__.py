import struct
import math
from cStringIO import StringIO

from bitstring import BitString

def _lefmt(bytes_length):
    if bytes_length == 2:
        return '<H'
    elif bytes_length == 4:
        return '<L'
    else:
        raise ValueError

def bytes2le(bytes):
    "byte string to LittleEndian"
    fmt = _lefmt(len(bytes))
    return struct.unpack(fmt, bytes)[0]

def le2bytes(i, length=4):
    "Little Endian to n Byte"
    fmt = _lefmt(length)
    return struct.pack(fmt, i)

def to_io(io_or_bytes):
    if isinstance(io_or_bytes, str):
        return StringIO(io_or_bytes)
    else:
        return io_or_bytes

class SWFParseError(Exception):
    """Raised when fairue swf binary parse"""

class StructRect:
    def __init__(self, io_or_bytes):
        io = to_io(io_or_bytes)

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

class SWFTag:
    names = {
        0:  'End',
        1:  'ShowFrame',
        2:  'DefineShape',
        6:  'DefineBitsJPEG',
        8:  'JPEGTables',
        9:  'SetBackgoundColor',
        11: 'DefineText',
        12: 'DoAction',
        20: 'DefineBitsLossLess',
        21: 'DefineBitsJPEG2',
        22: 'DefineShape2',
        26: 'PlaceObject2',
        32: 'DefineShape3',
        35: 'DefineBitsJPEG3',
        36: 'DefineBitsLossless2',
        37: 'DefineEditText',
        39: 'DefineSprite',
        43: 'FrameLabel',
        48: 'DefineFont2',
        88: 'DefineFontName',
        }

    def __init__(self, io_or_bytes):
        io = io_or_bytes

        self.header_bytes = io.read(2)
        header_num = bytes2le(self.header_bytes)
        self.tag_type = header_num >> 6
        self.body_bytes_length = header_num & 0x3f
        if self.body_bytes_length == 0x3f:
            more_header = io.read(4)
            self.header_bytes += more_header
            self.body_bytes_length = bytes2le(more_header)
        self.body_bytes = io.read(self.body_bytes_length)
        
    def __len__(self):
        return len(self.header_bytes) + self.body_bytes_length

    def is_end(self):
        return self.tag_type == 0

    def is_long(self):
        return self.body_bytes_length > 0x3f

    def is_short(self):
        return not self.is_long()

    def type_name(self):
        return self.names.get(self.tag_type, 'Unknown')

    def build(self):
        return self.header_bytes + self.body_bytes
        
class SWF:
    def __init__(self, io_or_bytes):
        io = to_io(io_or_bytes)

        self.signature = io.read(3)
        self.version   = ord(io.read(1))
        self.filesize  = bytes2le(io.read(4))

        self.frame_size  = StructRect(io)
        self.frame_rate  = bytes2le(io.read(2)) / 0x100
        self.frame_count = bytes2le(io.read(2))

        self.tags = []
        tag = None
        while tag is None or not tag.is_end():
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
               struct.pack('b', self.version) +  \
               le2bytes(self.filesize, 4) + \
               self.frame_size.build() + \
               le2bytes(self.frame_rate * 0x100, 2) + \
               le2bytes(self.frame_count, 2)
        
    def build(self):
        return self.build_header() + ''.join(tag.build() for tag in self.tags)
