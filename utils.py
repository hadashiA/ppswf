import struct
from array import array
from cStringIO import StringIO
import math

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

def AttrAccessor(function):
    return property(**function())

def in_groups_of(n, values):
    length = len(values)
    if isinstance(values, str):
        numbers = array('B')
        numbers.fromstring(values)
    else:
        numbers = values
    
    return tuple(
        tuple(numbers[i:i+n]) for i in range(0, length - 1, n)
        )
        
def rgb(rgb_bytes):
    return in_groups_of(3, rgb_bytes)

def rgba(rgba_bytes):
    return in_groups_of(4, rgba_bytes)

def indices(bytes):
    a = array('B')
    a.fromstring(bytes)
    return a

def adjust_indices_bytes(pallete_bytes, width):
    result = ""
    
    alex_width = (width + 3) & -4
    gap = alex_width - width
    for i in range(0, len(pallete_bytes), width):
        result += pallete_bytes[i:i+width] + ('\x00' * gap)
    return result
