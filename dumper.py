import sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.basename(current_dir) == 'ppswf':
    sys.path.append(
        os.path.realpath(os.path.join(current_dir, '..'))
        )

from ppswf import SWF

def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        io = open(os.path.abspath(path))
        swf = SWF(io)

        print '---- Reading the file header ----'
        print swf.signature
        print 'File version    ', swf.version
        print 'File size       ', swf.filesize
        print 'Movie width     ', swf.width
        print 'Movie height    ', swf.height
        print 'Frame rate      ', swf.frame_rate
        print 'Frame count     ', swf.frame_count

        print '---- Reading movie details ----'
        for tag in swf.tags:
            print tag
        
    else:
        print "usage python swf.py <input.swf>"
    
if __name__ == '__main__':
    main()
