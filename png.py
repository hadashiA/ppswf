import struct
from cStringIO import StringIO

import utils

class PNGParseError:
    """Raised when cannt png parse"""

class PNG:
    SIGNATURE = '\x89PNG\r\n\x1a\n'

    __filterd_idat = ''
    __idat = None

    alpha_bytes = None

    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        signature, = struct.unpack('8s', io.read(8))
        if signature != PNG.SIGNATURE:
            raise PNGParseError, 'Not PNG'

        chunk_name = None
        while chunk_name not in ('IEND', ''):
            chunk_header = io.read(8)
            chunk_length, chunk_name = struct.unpack('>L4s', chunk_header)
            chunk_data = io.read(chunk_length)
            chunk = getattr(self, chunk_name, self.UNKNOWN)
            chunk(chunk_data, chunk_length)
            crc = io.read(4)            # skip verify

    def UNKNOWN(self, data, length):
        pass

    def IHDR(self, data, length):
        self.width, self.height, \
        self.depth, self.color_type, \
        self.compress_type, self.filter_type, self.interace_type = \
          struct.unpack('>LLBBBBB', data)

    def PLTE(self, data, length):
        self.pallete_bytes = data
        self.pallete_size  = length / 3

    def IDAT(self, data, length):
        self.__filterd_idat += data.decode('zlib')

    def IEND(self, data, length):
        pass

    def tRNS(self, data, length):
        self.alpha_bytes = data
            
    @property
    def idat(self):
        if self.__idat is None:
            self.__idat = ''
            io = StringIO(self.__filterd_idat)
            first_column = io.read(1)
            while first_column:
                filter_type = ord(first_column)
                if filter_type == 0:
                    self.__idat += io.read(self.width)

                first_column = io.read(1)
            del self.__filterd_idat

        return self.__idat

    def with_pallete(self):
        return self.color_type == 3

    def with_transparent(self):
        return self.alpha_bytes or self.color_type in (4, 6)

    def build_pallete(self):
        if self.with_pallete():
            return self.pallete_bytes

    def build_indices(self):
        if self.with_pallete():
            return self.idat

    def build_xrgb(self):
        # using pallete
        if self.color_type == 3:
            result = ''
            for byte in self.idat:
                index = ord(byte) * 3
                result += '\x00' + self.pallete_bytes[index:index+3]
            return result
        else:
            raise NotImplementedError

    def build_argb(self):
        # using pallete
        if self.color_type == 3:
            result = ''
            for byte in self.idat:
                index = ord(byte) * 3
                result += '\x00' + self.pallete_bytes[index:index+3]
            return result
        else:
            raise NotImplementedError
