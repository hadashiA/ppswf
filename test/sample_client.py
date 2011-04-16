import sys
import os

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')

sys.path.append(root_dir)
swf_path  = os.path.join(fixtures_dir, 'orz.swf')
jpeg_path = os.path.join(fixtures_dir, 'gogopher_2.jpg')

# sys.path.append(os.path.expanduser('~/dev/naraku'))

from ppswf import SWF
from ppswf import swftag

def main():
    swf = SWF(open(swf_path).read())

    # bg_tag = swf.find_tag(swftag.SetBackgroundColor)
    # bg_tag.rgb = (255,0,0)
    swf.tags[0] = swftag.SetBackgroundColor(rgb=(255,0,0))

    # jpeg_tag = swf.images[1]
    # # jpeg_tag = swf.find_tag(swftag.DefineBitsJPEG2)
    # jpeg_tag.image = open(jpeg_path).read()

    out_dir = os.path.expanduser('~/tmp')
    open(os.path.join(out_dir, 'orz2.swf'), 'w').write(swf.build())

if __name__ == '__main__':
    main()
