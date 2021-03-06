import sys
import os

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
fixtures_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')

sys.path.append(root_dir)
swf_path  = os.path.join(fixtures_dir, 'orz.swf')
jpeg_path = os.path.join(fixtures_dir, 'gogopher_2.jpg')
red_path  = os.path.join(fixtures_dir, 'red.gif')
gif_path  = os.path.join(fixtures_dir, 'gogopher.gif')
png_path  = os.path.join(fixtures_dir, 'gogopher.png')
# png_path  = os.path.join(fixtures_dir, 'red.png')
# gif_path  = os.path.expanduser('~/tmp/unko.gif')
# sys.path.append(os.path.expanduser('~/dev/naraku'))

import ppswf
from ppswf import swftag

def main():
    swf = ppswf.SWF(open(swf_path).read())

    # bg_tag = swf.find_tag(swftag.SetBackgroundColor)
    # bg_tag.rgb = (255,0,0)
    # swf.tags[0] = swftag.SetBackgroundColor(rgb=(255,0,0))

    # jpeg_tag = swf.images[1]
    # jpeg_bytes = open(jpeg_path).read()
    # # jpeg_tag = swf.find_tag(swftag.DefineBitsJPEG2)
    # jpeg_tag.image = jpeg_bytes
    # jpeg_tag = swftag.DefineBitsJPEG2(jpeg=jpeg_bytes)

    # swf.images[1] = jpeg_tag

    # swf.images[1] = ppswf.JPEG(open(jpeg_path))
    # swf.images[1] = ppswf.GIF(open(gif_path))
    swf.images[1] = ppswf.PNG(open(png_path))

    out_dir = os.path.expanduser('~/tmp')
    open(os.path.join(out_dir, 'orz2.swf'), 'w').write(swf.build())

if __name__ == '__main__':
    main()




