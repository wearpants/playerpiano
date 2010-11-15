import sys

outfile = None

def write(s):
    """write s to stdout"""
    s = s.replace('\n', '\r\n')
    outfile.write(s)
    outfile.flush()

def make_target(options):
    global outfile
    outfile = open(options.dup, 'wb', 0)
    return write
    
def free_target():
    outfile.close()
