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
import optparse
import re
import os.path

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
    
banner = '''Python %s on %s\nType "help", "copyright", "credits" or "license" for more information.\n'''%(sys.version, sys.platform)

doctest_re=re.compile('# *doctest.*$')

if sys.version_info[0] == 2:
    def load_testfile(filename):
        return doctest._load_testfile(filename, None, False)
else:
    # For python3 compatibility
    def load_testfile(filename):
        return doctest._load_testfile(filename, None, False, 'utf8')

# based on doctest.testfile
def doctests_from_text(filename, encoding=None):

    # Relativize the path
    text, filename = load_testfile(filename)

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

usage = \
"""Usage: %s <options> <FILE> 

PlayerPiano amazes your friends by running Python doctests
in a fake interactive shell.

FILE can either be a module name or the path to a text file.
Press: <random_keys> to 'type' source   <EOF> to exit at the end
       <enter> to show results.         <^C> to break.
"""%os.path.basename(sys.argv[0])


targets = {} # places we write to

def write(s):
    for t in targets.values():
        t(s)

def main():
    
    optparser = optparse.OptionParser(usage = usage)
    optparser.add_option("--fifo", dest="fifo", action="store", default=None,
    help="duplicate output to a fifo")
    optparser.add_option("--no-terminal", dest="terminal", action="store_false", default=True,
    help="disable output on main terminal")    
    optparser.add_option("--color", dest="color", action="store_true", default=False,
    help="enable color")
    
    options, args = optparser.parse_args()
    
    if len(args) != 1:
        optparser.print_help()
        sys.exit(1)

    if options.terminal:
        from playerpiano import terminal_target
        targets[terminal_target] = terminal_target.make_target(options)

    if options.fifo:
        from playerpiano import fifo_target
        targets[fifo_target] = fifo_target.make_target(options)

    if options.color:
        from playerpiano.terminal_highlighter import highlight as _highlight
        

    fname=args[0]
    
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

        for test in tests:
            for example in test.examples:
                char_count = 0 
                want = example.want
                source = example.source
                
                # strip doctest directives
                source = doctest_re.sub('', source)

                # highlight
                if options.color:
                    source = _highlight(source)

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
        for t in list(targets.keys()):
            del targets[t]
            t.free_target()

if __name__ == '__main__':
    main()
