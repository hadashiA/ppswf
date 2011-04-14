import struct

def _lefmt(bytes_length):
    if bytes_length == 2:
        return '<H'
    elif bytes_length == 4:
        return '<L'
    else:
        raise ValueError

def bytes2le(bytes):
    "byte string to LittleEndian"
    fmt = _lefmt(len(bytes))
    return struct.unpack(fmt, bytes)[0]

def le2bytes(i, length=4):
    "Little Endian to n Byte"
    fmt = _lefmt(length)
    return struct.pack(fmt, i)

def bytes2be(i, length=2):
    return 1
