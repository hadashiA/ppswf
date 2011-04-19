import struct
import math
from cStringIO import StringIO

from bitstring import BitString

class GIFParseError(Exception):
    """Raised when fairue gif parse"""

def DATA(io):
    data = ''
    block_size = None
    while block_size != 0x00:
        byte = io.read(1)
        if not byte:
            return data
        block_size = ord(byte)
        data += io.read(block_size)
        
    return data

class ImageBlock:
    SEPARATER = 0x2c

    def __init__(self, io, gif):
        self.left_pos, self.top_pos, self.width, self.height, self.flags = \
          struct.unpack('<HHHHB', io.read(9))

        if self.pallete_flag:
            self.pallete_size  = 2 ** ((self.flags & 0x7) + 1)
            self.pallete_bytes = io.read(self.pallete_size * 3)
        else:
            self.pallete_size  = gif.pallete_size
            self.pallete_bytes = gif.pallete_bytes

        self.lzw_min_code_size = ord(io.read(1))
        self.lzwdata_bytes = DATA(io)

    @property
    def pallete_flag(self):
        return bool(self.flags >> 7)

    @property
    def interlace_flag(self):
        return bool((self.flags >> 6) & 1)

    @property
    def sort_flag(self):
        return bool((self.flags >> 5) & 1)
        
class GraphicControlExtension:
    LABEL = 0xf9

    def __init__(self, io):
        self.block_size = ord(io.read(1))
        if self.block_size != 0x04:
            raise GIFParseError

        self.flags, self.delay_time, self.transparent_color_index, end = \
          struct.unpack('<BHBB', io.read(5))

        if end != 0x00:
            raise GIFParseError

# class CommentExtension:
#     LABEL = 0xfe

#     def __init__(self, io):
#         pass

class UnknownExtension:
    def __init__(self, io):
        byte = None
        while byte != 0x00:
            byte = ord(io.read(1))

EXTENSION_INTRODUCER = 0x21
EXTENSION_END = 0x00

# extension_types = [GraphicControlExtension, CommentExtension]
extension_types = [GraphicControlExtension]
extension_types_for_label = dict((extension_type.LABEL, extension_type)
                                 for extension_type in extension_types)

def Extension(io):
    label = ord(io.read(1))
    extension_type = extension_types_for_label.get(label, UnknownExtension)
    return extension_type(io)

class GIF:
    __pallete_rgb = None

    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        self.signature, self.version, self.width, self.height, \
        self.flags, \
        self.bgcolor_index, self.pixcel_aspect_ratio = \
          struct.unpack('<3s3sHHBBB', io.read(13))

        if self.pallete_flag:
            self.pallete_bytes = io.read(self.pallete_size * 3)

        self.blocks = []
        self.images = []
        while True:
            next_byte = ord(io.read(1))
            if next_byte == 0x3b:
                return

            elif next_byte == ImageBlock.SEPARATER:
                image_block = ImageBlock(io, self)
                self.blocks.append(image_block)
                self.images.append(image_block)

            elif next_byte == EXTENSION_INTRODUCER:
                self.blocks.append(Extension(io))
                
    @property
    def pallete_flag(self):
        return bool(self.flags >> 7)

    @property
    def color_resolution(self):
        return ((self.flags >> 4) & 0x7) + 1

    @property
    def sort_flag(self):
        return bool((self.flags >> 3) & 0x8)

    @property
    def pallete_size(self):
        return 2 ** ((self.flags & 0x7) + 1)
