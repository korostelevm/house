import tornado.ioloop
import tornado
import tornado.web
import json
import os
from requests.sessions import session
os.environ['TZ'] = 'US/Eastern'


import traceback


import json
import time
import datetime


import time
import socket
import base64

src     = '192.168.1.100'       # ip of remote
mac     = '00-AB-11-11-11-11' # mac of remote
remote  = 'python remote'     # remote name
dst     = '192.168.1.19'       # ip of tv

app_     = 'python'            # iphone..iapp.samsung
# tv      = 'LE32C650'          # iphone.LE32C650.iapp.samsung
tv      = 'UN55ES6160'          # iphone.LE32C650.iapp.samsung


import eiscp
import datetime

# Create a receiver object, connecting to the host


def timestamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')



def push(key):
    print key
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.connect((dst, 55000))
    msg = chr(0x64) + chr(0x00) +\
        chr(len(base64.b64encode(src)))    + chr(0x00) + base64.b64encode(src) +\
        chr(len(base64.b64encode(mac)))    + chr(0x00) + base64.b64encode(mac) +\
        chr(len(base64.b64encode(remote))) + chr(0x00) + base64.b64encode(remote)
    print msg
    pkt = chr(0x00) +\
        chr(len(app_)) + chr(0x00) + app_ +\
        chr(len(msg)) + chr(0x00) + msg
    print pkt
    print new.send(pkt)
    msg = chr(0x00) + chr(0x00) + chr(0x00) +\
        chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
    pkt = chr(0x00) +\
        chr(len(tv))  + chr(0x00) + tv +\
        chr(len(msg)) + chr(0x00) + msg
    print new.send(pkt)
  
    print new.close()
    time.sleep(0.1)
    
def xbox():
    push('KEY_TV')
    time.sleep(0.2)
    push('KEY_SOURCE')
    time.sleep(0.2)
    push('KEY_DOWN')
#    time.sleep(0.2)
#    push('KEY_DOWN')
    time.sleep(0.2)
    push('KEY_ENTER')
    

def antenna():
    push('KEY_TV')
    time.sleep(0.1)
    push('KEY_ENTER')

def vol(direction, num_range=False):
    
    print num_range
    print num_range
    print num_range
    print num_range
    
    if direction == 'mute':
        push('KEY_MUTE')
    if  direction == 'up':
        push('KEY_VOLUP')
    if  direction == 'down':
        push('KEY_VOLDOWN')
    
    if  direction == 'downrange':
        for i in range(0,int(num_range)):
            push('KEY_VOLDOWN')
            
    if  direction == 'uprange':
        for i in range(0,int(num_range)):
            push('KEY_VOLUP')

        
    time.sleep(0.1)

def tv_power(arg):
	print 'got tv_power', arg, timestamp()
	push('KEY_POWEROFF')
	time.sleep(0.2)

receiver = eiscp.eISCP('192.168.1.16')

def onkyo_source(source):
	print 'got onkyo source', source, timestamp()
	if source.lower() == 'xbox':
		source = 'game'

	receiver.command('source '+source.lower())

	receiver.disconnect()


def onkyo_vol(vol):
	print 'got onkyo vol', vol, timestamp()
	receiver.command('volume '+vol)

	

class TVHandler(tornado.web.RequestHandler):
    
    
    
    def check_origin(self, origin):
        return True
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    #
    


    def get(self):
#        key = self.get_argument("key")
        f = self.get_argument("f")
        arg=self.get_argument("arg", True, None)
#         if key:
#             push('KEY_'+key)







        if f == 'stereo_source':
        	onkyo_source(arg)

        if f == 'stereo_vol':
        	onkyo_vol(arg)
        if f == 'stereo_cec':
        	onkyo_cec(arg)


        if f == 'tv_power':
            tv_power(arg)
        
        
        
        res = {'f':f,'arg':arg}
        
        self.write(json.dumps(res))
#        self.render("index.html")





def make_app():
    return tornado.web.Application([
#        (r'/', tornado.web.StaticFileHandler,  {'path':'index.html'}),
        (r"/tv*", TVHandler),
#        (r'/(.*)', tornado.web.StaticFileHandler, {'path': './public'}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': 'index.html'}),
        
    ],compress_response=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(83)
    server = tornado.ioloop.IOLoop.instance()
    server.start()
#     tornado.ioloop.IOLoop.current().start()