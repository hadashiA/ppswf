import math
from cStringIO import StringIO

from bitstring import BitString

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

class Matrix:
    def __init__(self, bits):
        bits.bytealign()
        start_pos = bits.tellbyte()

        self.has_scale = bool(bits.readbits(1).uint)
        if has_scale:
            scale_bits_length = bits.readbits(5).uint
            self.scale_x = bits.readbits(scale_bits_length).uint
            self.scale_y = bits.readbits(scale_bits_length).uint
        else:
            self.scale_x = 20
            self.scale_y = 20

        self.has_rotate = bool(bits.readbits(1).uint)
        self.rotate_skew = []
        if self.has_rotate:
            rotate_bits_length = bits.readbits(5).uint
            self.rotate_skew[0] = bits.readbits(rotate_bits_length).uint
            self.rotate_skew[1] = bits.readbits(rotate_bits_length).uint
        else:
            self.rotate_skew[0] = 0
            self.rotate_skew[1] = 0

        translate_bits_length = bits.readbits(5).uint
        self.translate_x = bits.readbits(translate_bits_length).uint
        self.translate_y = bits.readbits(translate_bits_length).uint

        bits.bytealign()
        self.__bytes_length = bits.tellbyte() - start_pos

    def __len__(self):
        return self.__bytes_length


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

