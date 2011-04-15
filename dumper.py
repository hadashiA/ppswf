import sys, os

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.basename(current_dir) == 'ppswf':
    sys.path.append(
        os.path.realpath(os.path.join(current_dir, '..'))
        )

def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        io = open(os.path.abspath(path))
        base, ext = os.path.splitext(path)

        if ext == '.swf':
            from ppswf import SWF
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
        
        elif ext in ('.jpg', '.jpeg'):
            import md5
            from ppswf.jpeg import JPEG, chunk_names
            
            jpeg = JPEG(io)

            print jpeg
            for chunk in jpeg.chunks:
                dump = "%s:" % chunk_names.get(chunk['marker'], 'Unknown')
                if 'length' in chunk:
                    dump += " length=%d" % chunk['length']
                if 'data' in chunk:
                    dump += "md5=%s" % md5.new(chunk['data']).hexdigest()
                print dump

        else:
            print "usage python swf.py <input.swf>"
    
if __name__ == '__main__':
    main()
