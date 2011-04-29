import struct
import zlib
from cStringIO import StringIO

from types import StructRect, FillStyles
from jpeg import JPEG, MARKER1, SOI, EOI
from gif import GIF
from png import PNG

from utils import AttrAccessor, adjust_indices_bytes, StructRect

class SWFTagBuildError(Exception):
    """Raised when fairue swf tag build"""

class SWFTagParseError(Exception):
   """Raised when fairue swf tag parse"""

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
            self.__header_bytes = struct.pack('<H',
                                              (self.CODE << 6) + \
                                              self.__body_bytes_length)
        else:                           # long
            self.__header_bytes = struct.pack('<HL',
                                              (self.CODE << 6) + 0x3f,
                                              self.__body_bytes_length)

        return self.__header_bytes

    def build(self):
        return self.build_header() + self._body_bytes

class SWFTagContent(SWFTagBase):
    CID_LENGTH = 2

    __cid = None

    @AttrAccessor
    def cid():
        def fget(self):
            if self.__cid is None and self._body_bytes is not None:
                self.__cid, = struct.unpack('<H', self._body_bytes[:self.CID_LENGTH])
            return self.__cid

        def fset(self, cid):
            self.__cid = cid or 0
            packed_cid = struct.pack('<H', self.__cid)
            if self._body_bytes is None:
                self._body_bytes = packed_cid
            else:
                self._body_bytes = packed_cid + self._body_bytes[self.CID_LENGTH:]

        return locals()

class SWFTagImage(SWFTagContent):
    pass

class Unknown(SWFTagBase):
    pass

class End(SWFTagBase):
    CODE = 0

class ShowFrame(SWFTagBase):
    CODE = 1

class DefineShape(SWFTagContent):
    CODE = 2

    __bits        = None
    __bounds      = None
    __fill_styles = None

    @property
    def bits(self):
        if self.__bits is None:
            self.__bits = BitString(bytes=self._body_bytes)
        return self.__bits

    @property
    def bounds(self):
        if self.__bounds is None:
            self.__bounds = StructRect(self._body_bytes[self.CID_LENGTH:])
        return self.__bounds

    @property
    def fill_styles(self):
        if self.__fill_styles is None:
            start_pos = self.CID_LENGTH + len(self.bounds)
            self.__fill_styles = FillStyles(self.bits[start_pos * 8:])

        return self.__fill_styles

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

    __image = None

    def __init__(self, image=None, cid=None, **kwargs):
        if image is not None:
            self.cid   = cid
            self.image = image
        else:
            super(DefineBitsLossless, self).__init__(**kwargs)

    @AttrAccessor
    def image():
        def fget(self):
            return self.__image

        def fset(self, image):
            if isinstance(image, GIF):
                image = image.images[0]

            if image.with_pallete():
                self.__image = image

                self._body_bytes = struct.pack('<HBHHB',
                                               self.cid or 0,
                                               3,
                                               image.width,
                                               image.height,
                                               image.pallete_size - 1,
                                               )
                self._body_bytes += zlib.compress(
                    image.pallete_bytes + \
                    adjust_indices_bytes(image.build_indices(),
                                         image.width))
            else:
                self._body_bytes = struct.pack('<HBHH',
                                               self.cid or 0,
                                               5,
                                               image.width,
                                               image.height,
                                               )
                self._body_bytes += zlib.compress(image.build_xrgb())

        return locals()

class DefineBitsJPEG2(SWFTagImage):
    CODE = 21

    def __init__(self, jpeg=None, cid=None, **kwargs):
        if jpeg is not None:
            self.cid = cid
            self.image = jpeg
        else:
            super(DefineBitsJPEG2, self).__init__(**kwargs)

    @AttrAccessor
    def image():
        def fget(self):
            return self._body_bytes

        def fset(self, jpeg):
            if isinstance(jpeg, JPEG):
                jpeg = jpeg.build()
            self._body_bytes = struct.pack('<HBBBB',
                                           self.cid or 0,
                                           MARKER1, SOI, MARKER1, EOI
                                           ) + jpeg

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
    header_num, = struct.unpack('<H', header_bytes)
    tag_code = header_num >> 6
    body_bytes_length = header_num & 0x3f
    if body_bytes_length == 0x3f:
        more_header = io.read(4)
        header_bytes += more_header
        body_bytes_length, = struct.unpack('<L', more_header)
    body_bytes = io.read(body_bytes_length)

    tag_type = tag_types_for_code.get(tag_code, Unknown)
    return tag_type(header_bytes=header_bytes,
                    body_bytes=body_bytes,
                    body_bytes_length=body_bytes_length)
