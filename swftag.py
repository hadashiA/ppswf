import struct

from utils import le2bytes, bytes2le
from jpeg import JPEG, MARKER1, SOI, EOI

class SWFTagBase(object):
    def __init__(self, header_bytes, body_bytes, body_bytes_length=None):
        self._header_bytes = header_bytes
        self._body_bytes   = body_bytes

        if body_bytes_length is not None:
            self._body_bytes_length = body_bytes_length
        else:
            self._body_bytes_length = len(body_bytes)

        self.filesize_changed = 0

    def __len__(self):
        return len(self._header_bytes) + self._body_bytes_length

    def is_long(self):
        return self._body_bytes_length > 0x3f

    def is_short(self):
        return not self.is_long()

    @property
    def tags(self):
        return []

    def build(self):
        return self._header_bytes + self._body_bytes

    def set_body_bytes_length(self, size=None):
        if size is None:
            size = len(self._body_bytes)

        if self.is_long():
            self._header_bytes = self._header_bytes[:2]
        header_num = bytes2le(self._header_bytes)

        if size < 0x3f:                 # short
            self._header_bytes = le2bytes((header_num & 0xffc0) + size, 2)
        else:                           # long
            self._header_bytes = le2bytes(header_num | 0x3f, 2) + le2bytes(size, 4)

        self.filesize_changed = (size - self._body_bytes_length )
        self._body_bytes_length = size

class End(SWFTagBase):
    pass

class ShowFrame(SWFTagBase):
    pass

class DefineShape(SWFTagBase):
    pass

class DefineBits(SWFTagBase):
    pass

class JPEGTables(SWFTagBase):
    pass

class SetBackgroundColor(SWFTagBase):
    def get_rgb(self):
        return self._body_bytes

    def set_rgb(self, rgb):
        self._body_bytes = struct.pack('BBB', *rgb)

    rgb = property(get_rgb, set_rgb)    

class DefineText(SWFTagBase):
    pass

class DoAction(SWFTagBase):
    pass

class DefineSound(SWFTagBase):
    pass

class DefineBitsLossless(SWFTagBase):
    pass

class DefineBitsJPEG2(SWFTagBase):
    def get_image(self):
        return self._body_bytes

    def cid(self):
        return bytes2le(self._body_bytes[0:2])

    def set_image(self, value):
        if isinstance(value, str):
            self._body_bytes = self._body_bytes[0:2]
            self._body_bytes += struct.pack('BBBB', MARKER1, SOI, MARKER1, EOI)
            self._body_bytes += value
            self.set_body_bytes_length()

    image = property(get_image, set_image)

class DefineShape2(SWFTagBase):
    pass

class PlaceObject2(SWFTagBase):
    pass

class RemoveObject2(SWFTagBase):
    pass

class DefineShape3(SWFTagBase):
    pass

class DefineButton2(SWFTagBase):
    pass

class DefineBitsJPEG3(SWFTagBase):
    pass

class DefineBitsLossless2(SWFTagBase):
    pass

class DefineEditText(SWFTagBase):
    pass

class DefineSprite(SWFTagBase):
    pass

class FrameLabel(SWFTagBase):
    pass

class SoundStreamHead2(SWFTagBase):
    pass

class DefineMorphShape(SWFTagBase):
    pass

class DefineFont2(SWFTagBase):
    pass

class DefineFontName(SWFTagBase):
    pass

def SWFTag(io):
    classes = {
        0:  End,
        1:  ShowFrame,
        2:  DefineShape,
        6:  DefineBits,
        8:  JPEGTables,
        9:  SetBackgroundColor,
        11: DefineText,
        12: DoAction,
        14: DefineSound,
        20: DefineBitsLossless,
        21: DefineBitsJPEG2,
        22: DefineShape2,
        26: PlaceObject2,
        28: RemoveObject2,
        32: DefineShape3,
        34: DefineButton2,
        35: DefineBitsJPEG3,
        36: DefineBitsLossless2,
        37: DefineEditText,
        39: DefineSprite,
        43: FrameLabel,
        45: SoundStreamHead2,
        46: DefineMorphShape,
        48: DefineFont2,
        88: DefineFontName,
        }
    
    if isinstance(io, str):
        io = StringIO(io)

    header_bytes = io.read(2)
    header_num = bytes2le(header_bytes)
    tag_code = header_num >> 6
    body_bytes_length = header_num & 0x3f
    if body_bytes_length == 0x3f:
        more_header = io.read(4)
        header_bytes += more_header
        body_bytes_length = bytes2le(more_header)
    body_bytes = io.read(body_bytes_length)

    return classes[tag_code](header_bytes=header_bytes,
                             body_bytes=body_bytes,
                             body_bytes_length=body_bytes_length)
