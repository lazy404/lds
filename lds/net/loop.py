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

class NetLoopThread(threading.Thread):
    def __init__(self, addr, port):
        threading.Thread.__init__(self)
        self.end=False
        
    def run(self):
        rec=ReceiverThread('225.0.0.2', 2000)
        rec.start()
        rq=rec.get_queue()
    
        while not self.end:
            print rq.get()
            
if __name__ == '__main__':
    s=NetLoopThread()
    #s.start()
    s.run()
