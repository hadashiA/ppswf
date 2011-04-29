import math
from cStringIO import StringIO

# from bitstring import BitString

from swftag import DefineShape2, DefineShape3

class StructRect:
    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

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


# SWF Shape inner structures

class Matrix:
    def __init__(self, bytes):
        io = StringIO(bytes)
        has_scale = io.read(1)

class FillStyles:
    def __init__(self, swftag_code, bytes):
        io = StringIO(bytes)

        count = ord(io.read(1))
        if count == 0xff and swftag_code > DefineShape2.CODE:
            count, = struct.unpack('<H', io.read(2))

        self.__content = []
        for i in range(count):
            fill_style = {}
            fill_style_type = ord(io.read(1))
            fill_style['type'] = fill_style_type
            if fill_style == 0x00:
                if swftag_code < DefineShape3.CODE:
                    fill_style['color'] = io.read(3)
                else:
                    fill_style['color'] = io.read(4)
            if fill_style in (0x10, 0x12):
                fill_style['gradient_matrix'] = None

        self.__bytes_length = io.tell()

    def __len__(self):
        return self.__bytes_length

    def __getitem__(self, i):
        pass

