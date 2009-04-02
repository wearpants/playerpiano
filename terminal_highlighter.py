import string 
import pygments
import pygments.lexers
import pygments.formatters

lexer = pygments.lexers.PythonLexer()
formatter = pygments.formatters.TerminalFormatter(bg="dark")

def highlight(source):
    # highlight
    source = pygments.highlight(source, lexer, formatter)
    # "fix it up"
    source = UselessColorFilter().process_string(source)
    return source

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

