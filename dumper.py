from ppswf import SWF

def main():
    import sys
    if len(sys.argv) == 2:
        path = sys.argv[1]
        import os
        io = open(os.path.abspath(path))
        swf = SWF(io)

        print '---- Reading the file header ----'
        print swf.signature
        print 'File version    ', swf.version
        print 'File size       ', swf.filesize
        print 'Movie width     ', (swf.x_max - swf.x_min)
        print 'Movie height    ', (swf.y_max - swf.y_min)
        print 'Frame rate      ', swf.frame_rate
        print 'Frame count     ', swf.frame_count

        print '---- Reading movie details ----'
        for tag in swf.tags:
            print tag.type_name()
        
    else:
        print "usage python swf.py <input.swf>"
    
if __name__ == '__main__':
    main()
