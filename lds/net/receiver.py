#
# encoding: utf-8
# (C) 2013 Michał Grzędzicki
#

import time
import struct
import socket
import sys
import threading, Queue

class ReceiverThread(threading.Thread):
    def __init__(self, addr, port):
        threading.Thread.__init__(self)
        self.outq=Queue.Queue(32)
        self.addr=addr
        self.port=port
        self.active=True

    def get_queue(self):
        return self.outq

    def end(self):
        self.active=False

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((self.addr, self.port))

        mreq = socket.inet_pton(socket.AF_INET, self.addr) + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while self.active:
            try:
                data, sender = s.recvfrom(1500)
                print time.time()
                self.outq.put((data,sender))
            except Queue.Empty, e:
                pass

if __name__ == '__main__':

    s=ReceiverThread('225.0.0.2', 2000)
    s.start()

    q=s.get_queue()

    while True:
        print q.get()
