from cStringIO import StringIO

from utils import le2bytes, bytes2le

class JPEGParseError(Exception):
    """Raised when fairue jpeg binary parse"""
    
class JPEG:
    def INVALID(io):
        raise JPEGParseError, 'invalid marker2'

    def SOI(io):
        return {
            'data': None,
            'lengh': None,
            }

    def EOI(io):
        return {
            'data': None,
            'length': None,
            }

    def SOS(io):
        return None

    def RST0(io):
        return None
    RST1 = RST2 = RST3 = RST0

    def RST4(io):
        # dynamic chunk marker
        return None
    RST5 = RST6 = RST7 = RST4

    def DEFAULT(io):
        length = io.read()

    marker_func_table = {
        0xD8: SOI,
        0xE0: 'APP0',  0xE1: 'APP1',  0xE2: 'APP2',  0xE3: 'APP3',
        0xE4: 'APP4',  0xE5: 'APP5',  0xE6: 'APP6',  0xE7: 'APP7',
        0xE8: 'APP8',  0xE9: 'APP9',  0xEA: 'APP10', 0xEB: 'APP11',
        0xEC: 'APP12', 0xED: 'APP13', 0xEE: 'APP14', 0xEF: 'APP15',
        0xFE: 'COM',
        0xDB: 'DQT',
        0xC0: 'SOF0', 0xC1: 'SOF1',  0xC2: 'SOF2',  0xC3: 'SOF3',
        0xC5: 'SOF5', 0xC6: 'SOF6',  0xC7: 'SOF7',
        0xC8: 'JPG',  0xC9: 'SOF9',  0xCA: 'SOF10', 0xCB: 'SOF11',
        0xCC: 'DAC',  0xCD: 'SOF13', 0xCE: 'SOF14', 0xCF: 'SOF15',
        0xC4: 'DHT',
        0xDA: SOS,
        0xD0: RST0, 0xD1: RST1, 0xD2: RST2, 0xD3: RST3,
        0xD4: RST4, 0xD5: RST5, 0xD6: RST6, 0xD7: RST7,
        0xDD: 'DRI',
        0xD9: EOI,
        0xDC: 'DNL',   0xDE: 'DHP',  0xDF: 'EXP',
        0xF0: 'JPG0',  0xF1: 'JPG1', 0xF2: 'JPG2',  0xF3: 'JPG3',
        0xF4: 'JPG4',  0xF5: 'JPG5', 0xF6: 'JPG6',  0xF7: 'JPG7',
        0xF8: 'JPG8',  0xF9: 'JPG9', 0xFA: 'JPG10', 0xFB: 'JPG11',
        0xFC: 'JPG12', 0xFD: 'JPG13',
        }

    def __init__(self, bytes):
        io = StringIO(bytes)
        self.chunks = []

        while marker1 = io.read(1):
            if marker1 != 0xFF:
                raise JPEGParseError, 'invalid marker1:0x%x' % marker1
            marker2 = io.read(1)
            chunk_type  = maker_func_table.get(marker2, INVALID)

            chunk = chunk_type(io)
            if chunk is not None:
                chunk['marker'] = marker2
                self.chunks.append(chunk)

            if chunk_type == EOI:
                return
