import struct
from cStringIO import StringIO

# from bitstring import BitString

from utils import AttrAccessor

class GIFParseError(Exception):
    """Raised when fairue gif parse"""

class GIF:
    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        self.signature, self.version, \
        self.width, self.height = struct.unpack('<3s3sHH', io.read(10))

        # self.flags = BitString(bytes=io.read(1))
        self.flags = ord(io.read(1))

        io.read(2)

    @AttrAccessor
    def global_color_table_flag():
        def fget(self):
            return self.flags >> 7

        def fset(self, value):
            value = 1 if value else 0
            self.flags &= (value << 7)

        return locals()

    @AttrAccessor
    def color_resolution():
        def fget(self):
            return ((self.flags >> 4) & 0x7) + 1

        def fset(self, value):
            if value > 8 or value < 1:
                raise ValueError
            self.flags &= ((value - 1) << 4)

        return locals()

    @AttrAccessor
    def sort_flag():
        def fget(self):
            return (self.flags >> 3) & 0x8

        def fset(self, value):
            value = 1 if value else 0
            self.flags &= (value << 3)
    
        return locals()

    @AttrAccessor
    def size_of_global_color_table():
        def fget(self):
            return self.flags & 0x7

        def fset(self, value):
            if value > 7 or value < 0:
                raise ValueError
            self.flags &= value
    
        return locals()
            
