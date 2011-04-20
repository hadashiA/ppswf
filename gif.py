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

class LZWDict:
    def __init__(self, kinds_count):
        self.kinds_count = kinds_count
        self.codes = [(None, i) for i in range(kinds_count)]

        self.clear_code = kinds_count
        self.codes.append(None)          # clear code

        self.end_code = kinds_count + 1
        self.codes.append(None)          # end code

        self.extra_codes = {}

    def clear(self):
        self.codes[self.end_code + 1:] = []
        self.extra_codes = {}
        
    def __len__(self):
        return len(self.codes)

    def __getitem__(self, pair):
        if pair[0] is None:
            return pair[1]
        else:
            return self.extra_codes[pair]

    def __iter__(self):
        return iter(self.codes)

    def append(self, pair):
        new_code = len(self.codes)
        self.extra_codes[pair] = new_code
        self.codes.append(pair)

    def build(self, code):
        code_1, code_2 = self.codes[code]
        if code_1:
            return self.build(code_1).append(code_2)
        else:
            return [code_2]
    

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

    # GIF LZW decode
    def pixels(self):
        result = []

        lzw_dict = LZWDict(self.pallete_size)
        bits = BitString(bytes=self.lzwdata_bytes)

        code_size = self.lzw_min_code_size + 1

        bits.readbits(code_size)
        prev_code = None
        while True:
            code = bits.readbits(code_size)
            if not code:
                break
            code = code.uint

            if code == lzw_dict.clear_code:
                lzw_dict.clear()
                code_size = self.lzw_min_code_size + 1
            elif code == lzw_dict.end_code:
                break
            else:
                print code, lzw_dict.codes
                # if code >= len(lzw_dict):
                if (prev_code, code) not in lzw_dict:
                    lzw_dict.append((prev_code, code))
                result += lzw_dict.build(code)

            prev_code = code

            if bits.tell() >= (2 ** code_size) and code_size < 12:
                code_size += 1

        return result
        
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
