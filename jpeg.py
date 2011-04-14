from cStringIO import StringIO

from utils import le2bytes, bytes2le, bytes2be

class JPEGParseError(Exception):
    """Raised when fairue jpeg binary parse"""
    
class JPEG:
    def PERIOD(io):
        return {
            'data': None,
            'lengh': None,
            }

    def PASS(io):
        return None

    def RST(io):
        while True:
            next_marker1 = io.read(1)
            if next_marker1 != 0xff:
                continue
            
            next_marker2 = io.read(1)
            if next_marker2 == 0x00:
                continue

    def DEFAULT(io):
        length = bytes2be(io.read(2))
        return {
            'data': io.read(length - 2),
            'length': length,
            }

    names = {
        0xd8: 'SOI',
        0xe0: 'APP0',  0xe1: 'APP1',  0xe2: 'APP2',  0xe3: 'APP3',
        0xe4: 'APP4',  0xe5: 'APP5',  0xe6: 'APP6',  0xe7: 'APP7',
        0xe8: 'APP8',  0xe9: 'APP9',  0xea: 'APP10', 0xeb: 'APP11',
        0xeC: 'APP12', 0xeD: 'APP13', 0xee: 'APP14', 0xef: 'APP15',
        0xfe: 'COM',
        0xdB: 'DQT',
        0xc0: 'SOF0', 0xc1: 'SOF1',  0xc2: 'SOF2',  0xC3: 'SOF3',
        0xc5: 'SOF5', 0xc6: 'SOF6',  0xc7: 'SOF7',
        0xc8: 'JPG',  0xc9: 'SOF9',  0xca: 'SOF10', 0xcb: 'SOF11',
        0xcc: 'DAC',  0xcd: 'SOF13', 0xce: 'SOF14', 0xcf: 'SOF15',
        0xc4: 'DHT',
        0xdA: 'SOS',
        0xd0: 'RST0', 0xd1: 'RST1', 0xd2: 'RST2', 0xd3: 'RST3',
        0xd4: 'RST4', 0xd5: 'RST5', 0xd6: 'RST6', 0xd7: 'RST7',
        0xdd: 'DRI',
        0xd9: 'EOI',
        0xdc: 'DNL',   0xde: 'DHP',  0xdf: 'EXP',
        0xf0: 'JPG0',  0xf1: 'JPG1', 0xf2: 'JPG2',  0xf3: 'JPG3',
        0xf4: 'JPG4',  0xf5: 'JPG5', 0xf6: 'JPG6',  0xf7: 'JPG7',
        0xf8: 'JPG8',  0xf9: 'JPG9', 0xfa: 'JPG10', 0xfb: 'JPG11',
        0xfc: 'JPG12', 0xfd: 'JPG13',
        }
    funcs = {
        0xd8: PERIOD,
        0xd9: PERIOD,
        0xda: PASS,
        0xd0: RST, 0xd1: RST, 0xd2: RST, 0xd3: RST,
        0xd4: RST, 0xd5: RST, 0xd6: RST, 0xd7: RST,
        }

    def __init__(self, bytes):
        io = StringIO(bytes)
        self.chunks = []

        while marker1 = io.read(1):
            if marker1 != 0xFF:
                raise JPEGParseError, 'invalid marker1:0x%x' % marker1
            marker2 = io.read(1)
            chunk_layout = funcs.get(marker2, DEFAULT)
            chunk = chunk_layout(io)
            if chunk is not None:
                chunk['marker'] = marker2
                self.chunks.append(chunk)

            if marker2 == 0xd9:
                return
