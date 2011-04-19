import struct

def AttrAccessor(function):
    return property(**function())

def rgb(pallete_bytes, pallete_size=None):
    if pallete_size is None:
        pallete_size = len(pallete_bytes)
    else:
        pallete_size *= 3

    numbers = struct.unpack('%dB' % pallete_size, pallete_bytes)
    return tuple(
        numbers[i:i + 3] for i in range(0, pallete_size - 1, 3)
        )

