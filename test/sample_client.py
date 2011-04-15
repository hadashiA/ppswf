import sys
import os

swf_path  = os.path.expanduser('~/dev/naraku/ppswf/test/fixtures/orz.swf')
jpeg_path = os.path.expanduser('~/dev/naraku/ppswf/test/fixtures/gogopher_2.jpg')

sys.path.append(os.path.expanduser('~/dev/naraku'))

from ppswf import SWF
from ppswf import swftag

def main():
    swf = SWF(open(swf_path).read())

    # bg_tag = swf.find_tag(swftag.SetBackgroundColor)
    # bg_tag.rgb = (255,0,0)

    jpeg_tag = swf.find_tag(swftag.DefineBitsJPEG2)
    # print "------ before"
    # print jpeg_tag._body_bytes_length
    # print len(jpeg_tag)
    # print swf.filesize
    
    # print "------ after"
    jpeg_tag.image = open(jpeg_path).read()
    # print jpeg_tag._body_bytes_length
    # print len(jpeg_tag)
    # swf.build_header()
    # print swf.filesize

    out_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'orz.swf')
    open(out_path, 'w').write(swf.build())

if __name__ == '__main__':
    main()
