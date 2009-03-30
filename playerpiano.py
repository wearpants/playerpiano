#!/usr/bin/env python
"""PlayerPiano amazes your friends by running Python doctests in a fake interactive shell.

author: Peter Fein 
email: pfein@pobox.com
homepage: http://playerpiano.googlecode.com/

Original idea & minor tty frobage from Ian Bicking.  Thanks Ian!
"""

import doctest
import termios
import tty
import sys
import re
import os.path

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

stdin_fd = None
old_mask = None

def frob_tty():
    """massage the terminal to not echo characters & the like"""
    global stdin_fd, old_mask
    stdin_fd = sys.stdin.fileno()
    old_mask = termios.tcgetattr(stdin_fd)
    new = old_mask[:]
    new[3] = new[3] & ~termios.ECHO # 3 == 'lflags'
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, new)
    tty.setraw(stdin_fd)

def eat_key():
    """consume a key.  Exit on ^C"""
    c = sys.stdin.read(1)
    if c == '\x03': # ^C
        sys.exit(1)
    else:
        return c

def restore_tty():
    """restore the terminal to its original state"""
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_mask)

def write(s):
    """write s to stdout"""
    s = s.replace('\n', '\r\n')
    sys.stdout.write(s)
    sys.stdout.flush()
    
banner = '''Python %s on %s\nType "help", "copyright", "credits" or "license" for more information.\n'''%(sys.version, sys.platform)

doctest_re=re.compile('# *doctest.*$')

# based on doctest.testfile
def doctests_from_text(filename, encoding=None):

    # Relativize the path
    text, filename = doctest._load_testfile(filename, None, False)

    name = os.path.basename(filename)

    if encoding is not None:
        text = text.decode(encoding)

    # Read the file, convert it to a test, and run it.
    test = doctest.DocTestParser().get_doctest(text, {}, name, filename, 0)
    
    return [test]


def doctests_from_module(modname):
    # need a fromlist b/c __import__ is stupid
    module = __import__(modname, globals(), {}, '__name__')    
    tests = doctest.DocTestFinder().find(module)
    return tests

def usage():
    print "Usage:", os.path.basename(sys.argv[0]), "FILE"
    print
    print "PlayerPiano amazes your friends by running Python doctests"
    print "in a fake interactive shell."
    print
    print "FILE can either be a module name or the path to a text file."
    print "Press: <random_keys> to 'type' source   <EOF> to exit at the end"
    print "       <enter> to show results.         <^C> to break." 
    
def main():
    
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    fname=sys.argv[1]
    
    if os.path.exists(fname):
        tests = doctests_from_text(fname)
    else:
        tests = doctests_from_module(fname)    
    
    try:
        frob_tty()

        # clear the screen to hide the command we were invoked with & write banner
        if sys.platform == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        write(banner)

        lexer = PythonLexer()
        formatter = TerminalFormatter(bg="dark")

        for test in tests:
            for example in test.examples:
                want = example.want
                source = example.source
                
                # strip doctest directives
                source = doctest_re.sub('', source)

                # highlight
                source = highlight(source, lexer, formatter)

                # strip trailing newline - added back below
                source = source.rstrip()
                
                # write out source code one keypress at a time
                write('>>> ')
                for s in source:
                    c = eat_key()
                    write(s)

                    if s == '\n':
                        write('... ')
                
                # slurp extra keys until <enter>
                while eat_key() != '\r':
                    pass
                
                # write out response, adding stripped newline first
                write('\n')
                write(want)
        
        # display final prompt & wait for <EOF> to exit
        write('>>> ')
        while eat_key() != '\x04': # ^D
            pass
        write('\n')
        
    finally:
        restore_tty()
        pass

if __name__ == '__main__':
    main()