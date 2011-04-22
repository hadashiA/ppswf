import struct
from array import array

def AttrAccessor(function):
    return property(**function())

def rgb(rgb_bytes, size=None):
    if size is None:
        size = len(rgb_bytes)
    else:
        size *= 3

    numbers = array('B')
    numbers.fromstring(rgb_bytes)
    return tuple(
        numbers[i:i + 3] for i in range(0, size - 1, 3)
        )

def rgba(rgba_bytes):
    size = len(rgba_bytes)
    numbers = array('B')
    array.fromstring(rgba_bytes)
    return tuple(
        numbers[i:i+4] for i in range(0, size - 1, 4)
        )

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
