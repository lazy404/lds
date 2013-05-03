#
# encoding: utf-8
# (C) 2013 Micha� Grz�dzicki
#

from time import time, sleep
import struct
import socket
import sys
import threading, Queue
from shortcrust.raspi.egl import EGL

from lds.gles.effects import *

class GLApp(threading.Thread):
    def __init__(self, timeline, event):
        threading.Thread.__init__(self)
	self.timeline=timeline
	self.event=event
	self.want_end=False
	self.egl=EGL(depthbuffer=True)
	self.w=self.egl.width
	self.h=self.egl.height

    def end(self):
	self.want_end=True

    def run(self):
	egl=self.egl

	glClearColor(0.0, 1.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	egl.swap_buffers()
	sleep(4)

	while not self.want_end:
	    tl=self.timeline.get_nowait()
	    tl.activate(self.w, self.h)

	    start_time=time()
	    end_time=start_time+tl.tlen
	    now=start_time
	    frames=0

	    while now <= end_time:
		tl.draw(now-start_time)
		egl.swap_buffers()
		frames+=1
		old=now
		now=time()
		if frames % 5 == 0:
		    print '%d' % int(1.0/(now-old))

	    print tl.name, 'done %d frames in %s seconds %d fps' % (frames, now-start_time, int(frames/(now-start_time)))


if __name__ == '__main__':
    tl=Queue.Queue()
    ev=Queue.Queue()
    

    s=GLApp(tl, ev)

    from lds.gles.shaders import *
    ps=PlasmaShader()
    ps2=PlasmaShader2()

    pl=Effect2D('plasma', s.w, s.h, 5.0,ps)

    pl2=Effect2D('plasma2', s.w, s.h, 10.0,ps2)

    tl.put(pl)
    tl.put(pl2)

    s.run()


    raw_input('end ?')
    #ev.put('ev')
    #sleep(3)
    s.end()