import ppswf

class SWFTagBase:
    def __init__(self, header_bytes, body_bytes, body_bytes_length=None):
        self.__header_bytes = header_bytes
        self.__body_bytes   = body_bytes

        if body_bytes_length is not None:
            self.body_bytes_length = body_bytes_length
        else:
            self.body_bytes_length = len(body_bytes)

    def __len__(self):
        return len(self.build_header()) + self.body_bytes_length

    def is_long(self):
        return self.__body_bytes_length > 0x3f

    def is_short(self):
        return not self.is_long()

    def build_header(self):
        return self.__header_bytes

    def build_body(self):
        return self.__body_bytes

    @property
    def tags(self):
        return []

    def build(self):
        return self.build_header() + self.build_body()

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
    pass

class DefineText(SWFTagBase):
    pass

class DoAction(SWFTagBase):
    pass

class DefineSound(SWFTagBase):
    pass

class DefineBitsLossless(SWFTagBase):
    pass

class DefineBitsJPEG2(SWFTagBase):
    pass

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

def SWFTag(io_or_bytes):
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
    
    io = ppswf.to_io(io_or_bytes)

    header_bytes = io.read(2)
    header_num = ppswf.bytes2le(header_bytes)
    tag_type = header_num >> 6
    body_bytes_length = header_num & 0x3f
    if body_bytes_length == 0x3f:
        more_header = io.read(4)
        header_bytes += more_header
        body_bytes_length = ppswf.bytes2le(more_header)
    body_bytes = io.read(body_bytes_length)

    return classes[tag_type](header_bytes=header_bytes,
                             body_bytes=body_bytes,
                             body_bytes_length=body_bytes_length)
        
