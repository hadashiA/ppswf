import struct
from cStringIO import StringIO

class FillStyles:
    def __init__(self, swftag_code, bytes):
        pos = 0

        self.__bytes_length = pos

    def __len__(self):
        return self.__bytes_length

    def __getitem__(self, i):
        pass
