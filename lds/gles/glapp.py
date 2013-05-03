#
# encoding: utf-8
# (C) 2013 Micha¸ Grz«dzicki
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
	glClearColor(0.0, 1.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
	self.egl.swap_buffers()

    def end(self):
	self.want_end=True

    def run(self):
	egl=self.egl

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
		#old=now
		now=time()
		#if frames % 5 == 0:
		#    print '%d' % int(1.0/(now-old))

	    print tl.name, 'done %d frames in %s seconds %d fps' % (frames, now-start_time, int(frames/(now-start_time)))


if __name__ == '__main__':
    tl=Queue.Queue()
    ev=Queue.Queue()

    s=GLApp(tl, ev)

    from lds.gles.shaders import *
    from lds.gles.texture import *

    ps=TexShader()

    t0=Texture('tex1.png')
    t0.activate(0)
    t0.load_texture()

    t1=Texture('tex2.png')
    t1.load_texture()
    t1.activate(1)

    t2=Texture('tex3.jpg')
    t2.load_texture()
    t2.activate(2)

    tl.put(Effect2D('plasma', s.w, s.h, 4.0,ps, [t0,t1]))
    tl.put(Pause(4.0))
    tl.put(Effect2D('plasma2', s.w, s.h, 5.0, ps, [t1,t2]))
    tl.put(Pause(1.0))
    tl.put(Effect2D('plasma3', s.w, s.h, 5.0, ps, [t2,t0]))

    #s.start()
    s.run()


    raw_input('end ?')
    s.end()
