import sys

def write(s):
    """write s to stdout"""
    s = s.replace('\n', '\r\n')
    sys.stdout.write(s)
    sys.stdout.flush()

def make_target(options):
    return write
    
def free_target():
    pass
