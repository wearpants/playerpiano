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
import argparse
import re
import os.path
import importlib
import contextlib

from . import terminal_highlighter, fifo_target, terminal_target


@contextlib.contextmanager
def frob_tty():
    """massage the terminal to not echo characters & the like"""
    stdin_fd = sys.stdin.fileno()
    old_mask = termios.tcgetattr(stdin_fd)
    new = old_mask[:]
    LFLAGS = 3
    new[LFLAGS] &= ~termios.ECHO
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, new)
    tty.setraw(stdin_fd)
    try:
        yield
    finally:
        # restore the terminal to its original state
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_mask)

def eat_key():
    """consume a key.  Exit on ^C"""
    c = sys.stdin.read(1)
    if c == '\x03': # ^C
        sys.exit(1)
    else:
        return c

banner = '''Python {sys.version} on {sys.platform}
Type "help", "copyright", "credits" or "license" for more information.
'''.format(**globals())

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
    module = importlib.import_module(modname)
    tests = doctest.DocTestFinder().find(module)
    return tests

targets = {} # places we write to

def write(s):
    for t in targets.values():
        t(s)

def run(tests, highlight):
    # clear the screen to hide the command we were invoked with & write banner
    if sys.platform == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    write(banner)

    for test in tests:
        for example in test.examples:
            want = example.want
            source = example.source

            # strip doctest directives
            source = doctest_re.sub('', source)

            # highlight
            source = highlight(source)

            # strip trailing newline - added back below
            assert source[-2] != '\r'
            if source[-1] == '\n':
                source = source[:-1]

            # write out source code one keypress at a time
            write('>>> ')
            for s in source:
                eat_key()
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


def main():
    """%(prog)s <options> <FILE>

    PlayerPiano amazes your friends by running Python doctests
    in a fake interactive shell.

    Press: <random_keys> to 'type' source   <EOF> to exit at the end
           <enter> to show results.         <^C> to break.
    """

    parser = argparse.ArgumentParser(usage=main.__doc__)
    parser.add_argument("--fifo", dest="fifo", action="store", default=None,
    help="duplicate output to a fifo")
    parser.add_argument("--no-terminal", dest="terminal", action="store_false", default=True,
    help="disable output on main terminal")
    parser.add_argument("--color", dest="color", action="store_true", default=False,
    help="enable color for Python 2")
    parser.add_argument("--color3", dest="color3", action="store_true", default=False,
    help="enable color for Python 3")
    parser.add_argument('file',
    help="either a module name or the path to a text file")
    options = parser.parse_args()

    if options.terminal:
        targets[terminal_target] = terminal_target.make_target(options)

    if options.fifo:
        targets[fifo_target] = fifo_target.make_target(options)

    if options.color:
        highlight = terminal_highlighter.highlight2
    elif options.color3:
        highlight = terminal_highlighter.highlight3
    else:
        highlight = lambda x: x

    if os.path.exists(options.file):
        tests = doctests_from_text(options.file)
    else:
        tests = doctests_from_module(options.file)

    try:
        with frob_tty():
            run(tests, highlight)
    finally:
        for t in list(targets.keys()):
            del targets[t]
            t.free_target()

if __name__ == '__main__':
    main()
