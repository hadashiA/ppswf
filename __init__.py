import struct
# import zlib
from cStringIO import StringIO

from bitstring import BitString

import utils
from inner_structures import StructRect
import swftag
from swftag import SWFTag
from gif import GIF
from png import PNG
from jpeg import JPEG

class SWFParseError(Exception):
    """Raised when fairue swf binary parse"""

class SWFImages:
    def __init__(self, owner):
        self.owner = owner
        self.__tags_for_cid_cache = None

    def __len__(self):
        return len(self.__tags_for_cid())

    def __iter__(self):
        return iter(self.__tags_for_cid().values())

    def __getitem__(self, cid):
        return self.__tags_for_cid()[cid]

    def __setitem__(self, cid, value):
        self.__tags_for_cid_cache = None
        index = None
        for i, tag in enumerate(self.owner.tags):
            if hasattr(tag, 'cid') and tag.cid == cid:
                index = i
                break

        if index is None:
            raise KeyError

        if issubclass(value.__class__, swftag.SWFTagBase):
            new_tag = value
        elif isinstance(value, JPEG):
            new_tag = swftag.DefineBitsJPEG2(value, cid=cid)
        elif value.with_transparent():
            # new_tag = swftag.DefineBitsLossless2(value, cid=cid)
            raise NotImplementedError
        else:
            new_tag = swftag.DefineBitsLossless(value, cid=cid)

        self.owner.tags[index] = new_tag

    def __tags_for_cid(self):
        if self.__tags_for_cid_cache is None:
            self.__tags_for_cid_cache =  dict((t.cid, t)
                                              for t in self.owner.tags
                                              if issubclass(t.__class__,
                                                            swftag.SWFTagImage))
        return self.__tags_for_cid_cache

    def cids(self):
        return self.__tags_for_cid().keys()

class SWF:
    __images = None

    def __init__(self, io):
        if isinstance(io, str):
            io = StringIO(io)

        self.signature, self.version, self.filesize = struct.unpack('<3sBL',
                                                                    io.read(8))
        self.frame_size  = StructRect(io)
        self.frame_rate, self.frame_count = struct.unpack('<HH', io.read(4))
        self.frame_rate /= 0x100

        # if self.is_compressed():
        #     body = io.read()
        #     io = StringIO(zlib.decompress(io.read()))
        #     self.signature = 'FWS'

        self.tags = []
        tag = None
        while tag is None or not isinstance(tag, swftag.End):
            tag = SWFTag(io)
            self.tags.append(tag)

    def is_compressed(self):
        if self.signature == 'CWS':
            return True
        elif self.signature == 'FWS':
            return False
        else:
            raise SWFParseError, 'invalid signature %s' % self.signature

    @property
    def x_min(self):
        return self.frame_size[0] / 20

    @property
    def x_max(self):
        return self.frame_size[1] / 20

    @property
    def y_min(self):
        return self.frame_size[2] / 20

    @property
    def y_max(self):
        return self.frame_size[3] / 20

    @property
    def width(self):
        return self.x_max - self.x_min

    @property
    def height(self):
        return self.y_max - self.y_min

    def build_header(self):
        # self.filesize += sum(tag.filesize_changed for tag in self.tags)
        self.filesize = 12 + len(self.frame_size) + sum(len(tag) for tag in self.tags)
        return struct.pack('<3sBL', self.signature, self.version, self.filesize) + \
               self.frame_size.build() + \
               struct.pack('<HH', self.frame_rate * 0x100, self.frame_count)
        
    def build(self):
        return self.build_header() + ''.join(tag.build() for tag in self.tags)

    def find_tag(self, cls):
        for tag in self.tags:
            if isinstance(tag, cls):
                return tag

    def find_tags(self, cls):
        return tuple(tag for tag in self.tags if isinstance(tag, cls))

    @property
    def images(self):
        if self.__images is None:
            self.__images = SWFImages(self)
        return self.__images
