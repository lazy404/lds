#
# encoding: utf-8
# (C) 2013 Michał Grzędzicki
#

import time
import struct
import socket
import sys
import threading, Queue

class SenderThread(threading.Thread):
    def __init__(self, addr, port, ttl=1):
        threading.Thread.__init__(self)
        self.inq=Queue.PriorityQueue(32)
        self.addr=addr
        self.port=port
        self.ttl=ttl
        self.active=True

    def get_queue(self):
        return self.inq

    def end(self):
        self.active=False

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl_bin = struct.pack('@i', self.ttl)

        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

        while self.active:
            try:
                (prio, data) = self.inq.get(timeout=5)
                s.sendto(data, (self.addr, self.port))

                self.inq.task_done()
            except Queue.Empty, e:
                pass

if __name__ == '__main__':
    s=SenderThread('225.0.0.2', 2000)
    s.start()
    from lds.net.proto import *
    q=s.get_queue()
    f="/usr/src/test.h264"
    #for i in range(100):
    i=1
    if True:
        q.put((0,struct.pack("!iBBBBB%ds" % len(f),VERSION,i,PREPARE_VIDEO,0,VIDEO_FULLSCREEN,len(f),f)))
        q.join()
        time.sleep(2)
        q.put((1,struct.pack("!iBBBBB",VERSION,i,RUN_VIDEO,0,VIDEO_FULLSCREEN,0)))
        q.join()

    s.end()
