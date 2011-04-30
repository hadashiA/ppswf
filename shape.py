import struct
from cStringIO import StringIO

from bitstring import BitString

import swftag

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

class FillStyle:
    SOLID                         = 0x00
    LINEAR_GRADIENT               = 0x10
    RADIAL_GRADIENT               = 0x12
    REPEATING_BITMAP              = 0x41
    NON_SMOOTHED_REPEATING_BITMAP = 0x42
    NON_SMOOTHED_CLIPPED_BITMAP   = 0x43

    def __init__(self, bits, tag):
        self.is_morph = tag.CODE in (swftag.DefineMorphShape.CODE,
                                     swftag.DefineShape4.CODE)
        self.type = bits.readbyte(1).uint
        if self.type == SOLID:
            if self.is_morph:
                self.color = [bits.readbyte(4), bits.readbyte(4)]
            elif tag.CODE < swftag.DefineShape3.CODE:
                self.color = bits.readbyte(3)
            else:
                self.color = bits.readbyte(4)

        elif self.type in (LINEAR_GRADIENT, RADIAL_GRADIENT):
            pass
                
        

class FillStyles:
    def __init__(self, bits, tag):
        pass

class LineStyle:
    def __init__(self, bits, tag):
        pass

class LineStyles:
    def __init__(self, bits, tag):
        pass
