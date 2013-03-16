#!/usr/bin/env python
# encoding: utf-8

import code
import sys
import os.path

class RecordingConsole(code.InteractiveConsole):
    """A python shell that records to the file `output`"""
    
    def __init__(self, output=None, *args, **kwargs):
        code.InteractiveConsole.__init__(self, *args, **kwargs)
        self.output = open(output, 'w')
    
    def raw_input(self, prompt):
        ri = code.InteractiveConsole.raw_input(self, prompt)
        self.output.write(prompt+ri+'\n')
        return ri

    def write(self, data):
        code.InteractiveConsole.write(self, data)
        self.output.write(data)

def main():
    if len(sys.argv) !=2:
        print("Usage: %s LOGFILE" % os.path.basename(sys.argv[0]))
    else:
        console = RecordingConsole(sys.argv[1])
        console.interact()

if __name__ == '__main__':
    main()
