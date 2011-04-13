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

        header_num = bytes2le(io.read(2))
        self.header_bits = BitString(int=header_num, length=16)
        self.tag_type = self.header_bits[0:10].uint
        self.body_bytes_length = self.header_bits[10:].uint
        if self.body_bytes_length == 0x3f:
            self.body_bytes_length = bytes2le(io.read(4))
        self.body_bytes = io.read(self.body_bytes_length)
        
    def __len__(self):
        return 2 + self.body_bytes_length

    def is_end(self):
        return self.tag_type == 0

    def is_long(self):
        return self.body_bytes_length > 0x3f

    def is_short(self):
        return not self.is_long()

    def type_name(self):
        return self.names.get(self.tag_type, 'Unknown')

    def build(self):
        header = le2bytes(self.tag_header_bit.int, 2)
        if self.is_long():
            header += '\x3f'
            header += le2bytes(self.body_bytes_length, 4)
        return header + self.body_bytes
        
class SWF:
    def __init__(self, io_or_bytes):
        io = to_io(io_or_bytes)

        self.signature = io.read(3)
        self.version   = ord(io.read(1))
        self.filesize  = bytes2le(io.read(4))

        frame_size = StructRect(io)
        self.x_min = frame_size[0] / 20
        self.x_max = frame_size[1] / 20
        self.y_min = frame_size[2] / 20
        self.y_max = frame_size[3] / 20

        self.frame_rate  = bytes2le(io.read(2)) / 0x100
        self.frame_count = bytes2le(io.read(2))

        self.header_bytes_length = 5 + len(frame_size) + 4

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

    def build(self):
        return ""
