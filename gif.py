import struct
import math
from cStringIO import StringIO

# from bitstring import BitString

# from utils import AttrAccessor

class GIFParseError(Exception):
    """Raised when fairue gif parse"""

class ImageBlock:
    SEPARATER = 0x2c

    def __init__(self, io):
        self.left_pos, self.top_pos, self.width, self.height, self.flags = \
          struct.unpack('<HHHHB', io.read(8))

        if self.pallete_flag:
            self.pallete_bytes = io.read(self.pallete_size * 3)

        self.lzw_min_code_size, self.lzwdata_bytes_length = \
          struct.unpack('BB', io.read(2))

        self.lzwdata_bytes = io.read(self.data_bytes_length)
        last = io.read(1)
        if last != 0x00:
            raise GIFParseError

    @property
    def pallete_flag(self):
        return bool(self.flags >> 7)

    @property
    def interlace_flag(self):
        return bool((self.flags >> 6) & 1)

    @property
    def sort_flag(self):
        return bool((self.flags >> 5) & 1)

    @property
    def pallete_size(self):
        return 2 ** ((self.flags & 0x7) + 1)
        

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
        while True:
            next_byte = io.read(1)
            if next_byte == 0x3b or not next_byte:
                return
            elif next_byte == ImageBlock.SEPARATER:
                self.blocks.append(ImageBlock(io))
                
    @property
    def pallete_flag(self):
        return bool(self.flags >> 7)
    # @AttrAccessor
    # def color_table_flag():
    #     def fget(self):
    #         return self.flags >> 7

    #     def fset(self, value):
    #         value = 1 if value else 0
    #         self.flags &= (value << 7)

    #     return locals()

    @property
    def color_resolution(self):
        return ((self.flags >> 4) & 0x7) + 1
    # @AttrAccessor
    # def color_resolution():
    #     def fget(self):
    #         return ((self.flags >> 4) & 0x7) + 1

    #     def fset(self, value):
    #         if value > 8 or value < 1:
    #             raise ValueError
    #         self.flags &= ((value - 1) << 4)

    #     return locals()

    @property
    def sort_flag(self):
        return bool((self.flags >> 3) & 0x8)
    # @AttrAccessor
    # def sort_flag():
    #     def fget(self):
    #         return (self.flags >> 3) & 0x8

    #     def fset(self, value):
    #         value = 1 if value else 0
    #         self.flags &= (value << 3)
    
    #     return locals()

    @property
    def pallete_size(self):
        return 2 ** ((self.flags & 0x7) + 1)
    # @AttrAccessor
    # def color_table_size():
    #     def fget(self):
    #         return 2 ** ((self.flags & 0x7) + 1)

    #     def fset(self, value):
    #         value = math.ceil(math.log(value, 2)) - 1
    #         self.flags &= value
    
    #     return locals()

    def pallete_rgb(self):
        if self.__pallete_rgb is not None:
            return self.__pallete_rgb

        numbers = struct.unpack('%dB' % self.pallete_size * 3, self.pallete_bytes)
        self.__pallete_rgb = tuple(
            numbers[i:i + 3] for i in range(0, (self.pallete_size * 3) - 1, 3)
            )
        return self.__pallete_rgb
            
