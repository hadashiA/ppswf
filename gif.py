import struct
import math
from cStringIO import StringIO

from bitstring import BitString

class GIFParseError(Exception):
    """Raised when fairue gif parse"""

EXTENSION_INTRODUCER = 0x21
EXTENSION_END = 0x00

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
    def __init__(self, bits_length):
        dict_size = 1 << bits_length
        self.codes = [(None, i) for i in range(dict_size)]

        self.clear_code = dict_size
        self.codes.append(None)          # clear code

        self.end_code = dict_size + 1
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
        if code >= len(self.codes):
            return None

        code_1, code_2 = self.codes[code]
        if code_1 is not None:
            return self.build(code_1) + chr(code_2)
        else:
            return chr(code_2)
    
# 10000100  #=> 100, 000, 10?
class LZWBitStream:
    def __init__(self, io):
        if isinstance(io, str):
            self.__io = StringIO(io)
        else:
            self.__io = io

        self.__buf = 0
        self.__buf_bits_length = 0
        self.__pos = 0

    def read(self, length):
        bit_mask = (1 << length) - 1

        while self.__buf_bits_length < length:
            byte = self.__io.read(1)
            if not byte:
                return None
            byte = ord(byte)
            self.__buf |= (byte << self.__buf_bits_length)
            self.__buf_bits_length += 8

        result = (bit_mask & self.__buf)
        self.__buf >>= length
        self.__buf_bits_length -= length

        self.__pos += length
        return result
    
    def tell(self):
        return self.__pos

class ImageBlock:
    SEPARATER = 0x2c

    def __init__(self, io, gif, graphic_control):
        self.graphic_control = graphic_control

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

    def with_pallete(self):
        return True

    def with_transparent(self):
        return self.graphic_control.transparent_flag

    def build_pallete(self):
        return self.pallete_bytes

    # GIF LZW decode
    def build_indices(self):
        result = ''

        code_size = self.lzw_min_code_size + 1

        lzw_dict = LZWDict(self.lzw_min_code_size)
        bits     = LZWBitStream(self.lzwdata_bytes)

        prev_code = None
        prev_data = ''

        code_size = self.lzw_min_code_size + 1

        while True:
            code = bits.read(code_size)

            if code is None or code == lzw_dict.end_code:
                break

            elif code == lzw_dict.clear_code:
                lzw_dict.clear()
                code_size = self.lzw_min_code_size + 1
                prev_code = bits.read(code_size)
                prev_data = lzw_dict.build(prev_code)
                result += prev_data

            else:
                data = lzw_dict.build(code)
                if data is None:
                    data = prev_data + prev_data[0]
                result += data
                lzw_dict.append((prev_code, ord(data[0])))
                prev_code, prev_data = code, data

            if len(lzw_dict) >= (1 << code_size) and code_size < 12:
                code_size += 1

        return result
        
class GraphicControlExtension:
    LABEL = 0xf9

    def __init__(self, io):
        self.block_size, \
        self.flags, self.delay_time, self.transparent_color_index, end = \
          struct.unpack('<BBHBB', io.read(6))

        if self.block_size != 0x04:
            raise GIFParseError

        if end != EXTENSION_END:
            raise GIFParseError

    @property
    def transparent_flag(self):
        return bool(self.flags & 1)

class CommentExtension:
    LABEL = 0xfe

    def __init__(self, io):
        self.data = DATA(io)
        end = ord(io.read(1))
        if end != EXTENSION_END:
            raise GIFParseError

class PlainTextExtension:
    LABEL = 0x01

    def __init__(self, io):
        self.block_size, \
        self.gird_left_pos, self.grid_top_pos, \
        self.grid_width, self.grid_height, \
        self.char_cell_width, self.char_cell_height, \
        self.fg_color_index, self.bg_color_index = \
          struct.unpack('<BHHHHBBBB', io.read(13))
        
        if self.block_size != 0x0c:
            raise GIFParseError

        self.data = DATA(io)
        end = ord(io.read(1))
        if end != EXTENSION_END:
            raise GIFParseError

class ApplicationExtension:
    LABEL = 0xff

    def __init__(self, io):
        self.block_size = ord(io.read(1))
        if self.block_size != 0x0b:
            raise GIFParseError

        self.identifier, self.authentication_code = struct.unpack('8s3s', io.read(11))
        self.data = DATA(io)

class UnknownExtension:
    def __init__(self, io):
        byte = None
        while byte != EXTENSION_END:
            byte = ord(io.read(1))

extension_types = [
    GraphicControlExtension,
    CommentExtension,
    PlainTextExtension,
    ApplicationExtension,
    ]
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
        self.bgcolor_index, self.aspect_ratio = \
          struct.unpack('<3s3sHHBBB', io.read(13))

        if self.signature != 'GIF':
            raise GIFParseError, 'Not GIF'

        if self.pallete_flag:
            self.pallete_bytes = io.read(self.pallete_size * 3)

        self.blocks = []
        self.images = []
        graphic_control = None
        while True:
            next_byte = io.read(1)
            if not next_byte:
                return
            next_byte = ord(next_byte)
            if next_byte == 0x3b:
                return

            elif next_byte == ImageBlock.SEPARATER:
                image_block = ImageBlock(io, self, graphic_control)
                self.blocks.append(image_block)
                self.images.append(image_block)
                graphic_control = None

            elif next_byte == EXTENSION_INTRODUCER:
                extension = Extension(io)
                if isinstance(extension, GraphicControlExtension):
                    graphic_control = extension
                self.blocks.append(extension)
                
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
