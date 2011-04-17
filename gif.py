import struct.pack, struct.unpack
import math.log, math.ceil
from cStringIO import StringIO

# from bitstring import BitString

# from utils import AttrAccessor

class GIFParseError(Exception):
    """Raised when fairue gif parse"""

class GIF:
    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        self.signature, self.version, self.width, self.height = \
          struct.unpack('<3s3sHH', io.read(10))

        # self.flags = BitString(bytes=io.read(1))
        self.flags = ord(io.read(1))

        self.bgcolor_index, self.pixcel_aspect_ratio = \
          struct.unpack('<HH', io.read(2))

        if self.is_pallete_on:
            self.pallete = io.read(self.pallete_size * 3)
        else:
            raise NotImplementedError

        self.blocks = []
        while True:
            next_byte = io.read(1)
            if next_byte == 0x3b:
                return
            elif next_byte == 0x2c:     # Imageblock
                struct.unpack('<HHHH')
                

    @property
    def is_pallete_on(self):
        return bool(slef.flags >> 7)
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
            
