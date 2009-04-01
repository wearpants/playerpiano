#!/usr/bin/env python
"""PlayerPiano amazes your friends by running Python doctests in a fake interactive shell.

author: Peter Fein 
email: pfein@pobox.com
homepage: http://playerpiano.googlecode.com/

Original idea & minor tty frobage from Ian Bicking.  Thanks Ian!
"""

import string

import stomp

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message

    def on_message(self, headers, message):
        print 'received headers %r message %s' % (headers, message)

conn = stomp.Connection()
conn.add_listener(MyListener())
conn.start()
conn.connect()

conn.subscribe(destination='/piano/keys', ack='auto')

def sendstomp(s):
    conn.send(s, destination='/piano/keys')



class UselessColorFilter(object):
    """a finite state machine that eats duplicate equivalent ANSi color codes, as should be 'obvious', from the source. -asheesh
    """
    def __init__(self):
        self.state = 'START'
        self.growing_color = ''
        self.last_color = None
    def handle_char(self, char):
        if self.state == 'START':
            if char in string.printable:
                # Always emit the color we have been growing; usually empty string
                return char
            else:
                assert char == '\x1b'
                assert self.growing_color == ''
                self.growing_color += char
                self.state = 'JUST_GOT_X1B'
        elif self.state == 'JUST_GOT_X1B':
            assert self.growing_color == '\x1b'
            assert char == '['
            self.growing_color += char
            self.state = 'GROWING_COLOR'
        elif self.state == 'GROWING_COLOR':
            if char == 'm':
                # Then the color is finished!
                # Was the color we just grew the last_color?
                # Tack on the space for good measure.
                self.growing_color += char

                final_color = self.growing_color
                should_print_this = (self.growing_color != self.last_color)

                # do some cleanup
                self.last_color = final_color
                self.growing_color = ''

                # We go back to the START
                self.state = 'START'

                if should_print_this:
                    return final_color
            else:
                self.growing_color += char

    def process_string(self, s):
        """"@yields a list of 1-char tokens, with a possible control code prefix
        
        FIXME: asheesh make me a generator.
        """
        generated = []
        for char in s:
            ret = self.handle_char(char)
            if ret is None:
                continue
            else:
                generated.append(ret)
        return generated


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
    sendstomp(s)
    
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

                # "fix it up"
                source = UselessColorFilter().process_string(source)

                # strip trailing newline - added back below
                assert source[-2] != '\r'
                if source[-1] == '\n':
                    source = source[:-1]
                
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
