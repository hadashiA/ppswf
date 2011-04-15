import struct

def __fmt(bytes_length):
    if bytes_length == 2:
        return 'H'
    elif bytes_length == 4:
        return 'L'
    else:
        raise ValueError

def bytes2le(bytes):
    "byte string to LittleEndian"
    return struct.unpack('<' + __fmt(len(bytes)), bytes)[0]

def le2bytes(i, length=4):
    "Little Endian to n bytes"
    return struct.pack('<' + __fmt(length), i)

def bytes2be(bytes):
    "byte string to BigEndian"
    return struct.unpack('>' + __fmt(len(bytes)), bytes)[0]
