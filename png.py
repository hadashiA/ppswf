import struct
from cStringIO import StringIO

import utils

class PNGParseError:
    """Raised when cannt png parse"""

class PNG:
    SIGNATURE = '\x89PNG\r\n\x1a\n'

    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        signature, = struct.unpack('8s', io.read(8))
        if signature != PNG.SIGNATURE:
            raise PNGParseError

        chunk_name = None
        while chunk_name != 'IEND':
            chunk_header = io.read(8)
            chunk_length, chunk_name = struct.unpack('>L4s', chunk_header)
            chunk_data = io.read(chunk_length)
            chunk = getattr(self, chunk_name, self.UNKNOWN)
            chunk(chunk_data)
            crc = io.read(4)

    def UNKNOWN(self, data):
        pass

    def IHDR(self, data):
        self.width, self.height, \
        self.depth, self.color_type, \
        self.compress_type, self.filter_type, self.interace_type = \
          struct.unpack('>LLBBBBB', data)

    def PLTE(self, data):
        self.pallete_bytes = data

    def IDAT(self, data):
        if not hasattr(self, '__idat'):
            self.__idat = ''
        self.__idat = data.decode('zlib')

    def IEND(self, data):
        pass

    def tRNS(self, data):
        self.alpha_pallete_bytes = data
            
    def build_xrgb(self):
        # using pallete
        if self.color_type == 3:
            result = ''
            for i, byte in enumerate(self.__idat):
                if i != 0 and (i % self.width != 0):
                    index = ord(byte) * 3
                    result += '\x00' + self.pallete_bytes[index:index+3]
            return result
        else:
            raise NotImplementedError
