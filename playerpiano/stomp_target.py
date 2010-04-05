import json
import stomp

class Stomper(object):
    def __init__(self, host, port):
        self.conn = stomp.Connection(host_and_ports=[(host, port)])
        self.conn.add_listener(MyListener())
        self.conn.start()
        self.conn.connect()

        self.conn.subscribe(destination='/piano/keys', ack='auto')
        
        self.char_num = 0 

    def send(self, s):
        self.char_num += len(s)
        self.conn.send(json.dumps({'text':s, 'char_num':self.char_num}),
                       destination='/piano/keys')

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message

stomper = None

def make_target(options):
    global stomper
    stomper = Stomper(options.stomp_host, options.stomp_port)
    return stomper.send

def free_target():
    global stomper
    if stomper is not None:
        stomper.stop() # XXX or whatever
        stomper = None
