import math
from cStringIO import StringIO

from bitstring import BitString

class StructRect:
    def __init__(self, bytes=None, bits=None):
        if bytes:
            if isinstance(bytes, str):
                io = StringIO(bytes)
            elif hasattr(bytes, 'read'):
                io = bytes
            else:
                raise TypeError, 'not readable object'

            first_byte = io.read(1)
            self.field_bits_length = ord(first_byte) >> 3
            bytes = first_byte + io.read(len(self) - 1)
            self.bits = BitString(bytes=bytes)

        elif bits:
            self.bits = bits
            self.field_bits_length = self.bits[:5].uint

    def __getitem__(self, i):
        begin = 5 + i * self.field_bits_length
        end   = 5 + (i + 1) * self.field_bits_length
        return self.bits[begin:end].uint

    def __len__(self):
        total_bits_length = 5 + (self.field_bits_length * 4)
        return int(math.ceil(total_bits_length / 8.0))

    def build(self):
        return self.bits.bytes
