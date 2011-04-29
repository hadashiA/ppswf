import struct
from array import array

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
