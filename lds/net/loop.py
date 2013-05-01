#
# encoding: utf-8
# (C) 2013 Micha¸ Grz«dzicki
#

import time
import struct
import socket
import sys
import threading, Queue

from lds.net.receiver import ReceiverThread
from lds.net.sender import SenderThread
from lds.net.proto import *
from lds.video.omxplayer import OmxPlayerThread

class NetLoopThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.want_end=False
	self.hfmt='!iBBBBB'
	self.hlen=struct.calcsize(self.hfmt)
    
    def end(self):
	self.rec.end()
	self.want_end=True

    def run(self):
        rec=ReceiverThread('225.0.0.2', 2000)
        rec.start()
        send=SenderThread('225.0.0.2', 2000)
        send.start()
	
        rq=rec.get_queue()
	sq=send.get_queue()

	self.rec=rec

        while not self.want_end:
            data=rq.get()

	    ver, cmdid, cmd, cmdflag, cmdopt , optlen= struct.unpack(self.hfmt, data[0][:self.hlen])

	    if optlen > 0:
		optstr = struct.unpack_from("%ds" % optlen, data[0], self.hlen)
	    else:
		optstr=False

	    if cmd == PREPARE_VIDEO:
		print 'got prepare', optstr
		self.vt=OmxPlayerThread(str(optstr))
		self.vt.start()
		self.vt.wait_ready()

	    if cmd == RUN_VIDEO:
		print 'got run'
		self.vt.play_video()
		self.vt.wait_ready()


if __name__ == '__main__':
    s=NetLoopThread()
    s.start()
    raw_input('end ?')
    s.end()
