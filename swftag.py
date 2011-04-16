import struct

from utils import le2bytes, bytes2le
from jpeg import JPEG, MARKER1, SOI, EOI

class SWFTagBase(object):
    __header_bytes      = None
    __body_bytes        = None
    __body_bytes_length = None

    def __init__(self, header_bytes, body_bytes, body_bytes_length=None):
        self.__header_bytes = header_bytes
        self._body_bytes    = body_bytes
        self.__body_bytes_length = body_bytes_length

    def __len__(self):
        return len(self.build_header()) + self.__body_bytes_length

    def is_long(self):
        return self.__body_bytes_length > 0x3f

    def is_short(self):
        return not self.is_long()

    @property
    def tags(self):
        return []

    def build_header(self, tag_code=None, body_bytes_length=None):
        # if not update
        if self.__header_bytes and tag_code is None and body_bytes_length is None:
            return self.__header_bytes

        if tag_code is None or body_bytes_length is None:
            header_num = bytes2le(self.__header_bytes)

        if tag_code is None:
            tag_code = header_num >> 6

        if body_bytes_length is None:
            body_bytes_length = header_num & 0x3f

        if body_bytes_length < 0x3f:    # short
            self.__header_bytes = le2bytes((tag_code << 6) + body_bytes_length, 2)
        else:                           # long
            self.__header_bytes = le2bytes((tag_code << 6) + 0x3f, 2) + \
                                  le2bytes(body_bytes_length, 4)
        self.__body_bytes_length = body_bytes_length

        return self.__header_bytes

    def build(self):
        return self.build_header() + self._body_bytes

    def is_image(self):
        return False

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
    def __init__(self, rgb=None, **kwargs):
        if rgb is not None:
            self.build_header(tag_code=9, body_bytes_length=3)
            self.rgb = rgb
        else:
            super(SetBackgroundColor, self).__init__(**kwargs)

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
    def is_image(self):
        return True

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

    def is_image(self):
        return True

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
    def is_image(self):
        return True

class DefineBitsLossless2(SWFTagBase):
    def is_image(self):
        return True

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
