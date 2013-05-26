#
# encoding: utf-8
# (C) 2013 Micha¸ Grz«dzicki
#

from time import time, sleep
import struct
import socket
import sys
import threading, Queue
from shortcrust.raspi.egl import EGL, opengles, openegl, eglints

from lds.gles.effects import *

class GLApp(threading.Thread):
    def __init__(self, timeline, event):
        threading.Thread.__init__(self)
	self.timeline=timeline
	self.event=event
	self.want_end=False

    def end(self):
	self.want_end=True

    def run(self, egl):

	#self.egl=EGL(depthbuffer=True)
	#egl=self.egl
	self.egl=egl
	#egl=self.egl

	self.w=self.egl.width
	self.h=self.egl.height

	glClearColor(0.2, 0.8, 0.2, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	egl.swap_buffers()

	while not self.want_end:
	    print 'waiting for effect ...'
	    tl=self.timeline.get()
	    print "doing: ", tl
	    s=time()
	    tl.activate(self.w, self.h)
	    print 'activate time', time()-s

	    start_time=time()
	    end_time=start_time+tl.tlen
	    now=start_time
	    frames=0

	    while now < end_time:
		if tl.draw(now-start_time):
		    egl.swap_buffers()

		frames+=1
		old=now
		now=time()
		if frames % 5 == 0:
		    print '%d' % int(1.0/(now-old))

	    if tl.draw(end_time-start_time):
		egl.swap_buffers()

	    print tl.name, 'done %d frames in %s seconds %d fps' % (frames, now-start_time, int(frames/(now-start_time)))


if __name__ == '__main__':
    tl=Queue.Queue()
    ev=Queue.Queue()

    egl=EGL(depthbuffer=True)

    s=GLApp(tl, ev)
    s.w=1080
    s.h=1920
    #s.start()

    #sleep(3)

    from lds.gles.shaders import *
    from lds.gles.texture import *

    ps=TexShader()
    ws=WrapShader()

    t0=Texture('tex1.png')
    t0.load_data()
    #t0.activate(0)

    t1=Texture('tex2.png')
    t1.load_data()
    #t1.activate(1)

    t2=Texture('tex3.jpg')
    t2.load_data()
    #t2.activate(2)



    tl.put(Effect2D('0-1', 3.0, ps, [t0,t1]))
    tl.put(Pause(1.0))

    tl.put(Effect2D('1-2', 3.0, ps, [t1,t2]))
    tl.put(Pause(1.0))

    #tl.put(Effect2D('2-0', 3.0, ps, [t2,t0]))
    #tl.put(Pause(2.0))

    #tl.put(Effect2D('0-1', 3.0, ps, [t0,t1]))
    #tl.put(Pause(2.0))

    #tl.put(Effect2D('1-2', 3.0, ps, [t1,t2]))
    #tl.put(Pause(2.0))

    tl.put(Effect2D('2-0', 3.0, ps, [t2,t1]))
    tl.put(Pause(2.0))
    tl.put(Effect2D('2-0', 5.0, ws, [t1,t1]))

    #o=OmxPlayer('/usr/src/test.h264', 0, 1536, 1080, 1920)
    #tl.put(o)

    s.run(egl)
    s.end()
