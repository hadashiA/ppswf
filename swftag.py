import struct

from utils import le2bytes, bytes2le
from jpeg import JPEG, MARKER1, SOI, EOI

def AttrAccessor(function):
    return property(**function())

class SWFTagBuildError(Exception):
    """Raised when fairue swf tag build"""

class SWFTagBase(object):
    __header_bytes      = None
    __body_bytes_length = None

    _body_bytes = None

    def __init__(self, header_bytes, body_bytes, body_bytes_length=None):
        self.__header_bytes      = header_bytes
        self.__body_bytes_length = body_bytes_length

        self._body_bytes = body_bytes

    def __len__(self):
        return len(self.build_header()) + self.__body_bytes_length

    def is_long(self):
        return self.__body_bytes_length > 0x3f

    def is_short(self):
        return not self.is_long()

    @property
    def tags(self):
        return []

    def build_header(self):
        body_bytes_length_now = len(self._body_bytes)
        if body_bytes_length_now == self.__body_bytes_length:
            if self.__header_bytes is not None:
                return self.__header_bytes
        else:
            self.__body_bytes_length = body_bytes_length_now

        if self.__body_bytes_length < 0x3f:    # short
            self.__header_bytes = le2bytes((self.CODE << 6) + \
                                           self.__body_bytes_length, 2)
        else:                           # long
            self.__header_bytes = le2bytes((self.CODE << 6) + 0x3f, 2) + \
                                  le2bytes(self.__body_bytes_length, 4)

        return self.__header_bytes

    def build(self):
        return self.build_header() + self._body_bytes

class SWFTagImage(SWFTagBase):
    __cid = None

    @AttrAccessor
    def cid():
        def fget(self):
            if self.__cid is not None:
                return self.__cid
            elif self._body_bytes:
                self.__cid = bytes2le(self._body_bytes[0:2])
                return self.__cid
            else:
                raise SWFTagBuildError, 'Cannt build body. Not known image cid.'

        def fset(self, cid):
            self.__cid = cid

        return locals()

class Unknown(SWFTagBase):
    pass

class End(SWFTagBase):
    CODE = 0

class ShowFrame(SWFTagBase):
    CODE = 1

class DefineShape(SWFTagBase):
    CODE = 2

class DefineBits(SWFTagBase):
    CODE = 6

class JPEGTables(SWFTagBase):
    CODE = 8

class SetBackgroundColor(SWFTagBase):
    CODE = 9

    def __init__(self, rgb=None, **kwargs):
        if rgb is not None:
            self.rgb = rgb
        else:
            super(SetBackgroundColor, self).__init__(**kwargs)

    @AttrAccessor
    def rgb():
        def fget(self):
            return self._body_bytes

        def fset(self, rgb):
            self._body_bytes = struct.pack('BBB', *rgb)

        return locals()


class DefineText(SWFTagBase):
    CODE = 11

class DoAction(SWFTagBase):
    CODE = 12

class DefineSound(SWFTagBase):
    CODE = 14

class DefineBitsLossless(SWFTagImage):
    CODE = 20

class DefineBitsJPEG2(SWFTagImage):
    CODE = 21

    def __init__(self, jpeg_bytes=None, cid=None, **kwargs):
        if jpeg_bytes is not None:
            self.cid = cid
            self.image = jpeg_bytes
            self.build_header()
        else:
            super(DefineBitsJPEG2, self).__init__(**kwargs)

    @AttrAccessor
    def image():
        def fget(self):
            return self._body_bytes

        def fset(self, value):
            if isinstance(value, str):
                self._body_bytes = le2bytes(self.cid, 2) + \
                                   struct.pack('BBBB', MARKER1, SOI, MARKER1, EOI) + \
                                   value

        return locals()

class DefineShape2(SWFTagBase):
    CODE = 22

class PlaceObject2(SWFTagBase):
    CODE = 26

class RemoveObject2(SWFTagBase):
    CODE = 28

class DefineShape3(SWFTagBase):
    CODE = 32

class DefineButton2(SWFTagBase):
    CODE = 34

class DefineBitsJPEG3(SWFTagImage):
    CODE = 35

class DefineBitsLossless2(SWFTagImage):
    CODE = 36

class DefineEditText(SWFTagBase):
    CODE = 37

class DefineSprite(SWFTagBase):
    CODE = 39

class FrameLabel(SWFTagBase):
    CODE = 43

class SoundStreamHead2(SWFTagBase):
    CODE = 45

class DefineMorphShape(SWFTagBase):
    CODE = 46

class DefineFont2(SWFTagBase):
    CODE = 48

class DefineFontName(SWFTagBase):
    CODE = 88

tag_types = [
    End,
    ShowFrame,
    DefineShape,
    DefineBits,
    JPEGTables,
    SetBackgroundColor,
    DefineText,
    DoAction,
    DefineSound,
    DefineBitsLossless,
    DefineBitsJPEG2,
    DefineShape2,
    PlaceObject2,
    RemoveObject2,
    DefineShape3,
    DefineButton2,
    DefineBitsJPEG3,
    DefineBitsLossless2,
    DefineEditText,
    DefineSprite,
    FrameLabel,
    SoundStreamHead2,
    DefineMorphShape,
    DefineFont2,
    DefineFontName,
    ]

tag_types_for_code = dict((tag_type.CODE, tag_type) for tag_type in tag_types)

def SWFTag(io):
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

    tag_type = tag_types_for_code.get(tag_code, Unknown)
    return tag_type(header_bytes=header_bytes,
                    body_bytes=body_bytes,
                    body_bytes_length=body_bytes_length)
