#
# encoding: utf-8
#
from shortcrust.shader import ShaderProgram
from shortcrust.buffer import AttributeBuffer
from shortcrust.gl2 import *
from time import sleep

from lds.video.omxplayer import OmxPlayerThread

class OmxPlayer(object):
    def __init__(self, fname, x1, y1, x2, y2):
	s=OmxPlayerThread(fname, x1, y1, x2, y2)
	s.start()
	s.wait_ready()
	self.s=s
	self.running=False
	self.tlen=50
	self.name=fname
	

    def draw(self, time):
	if not self.running:
	    self.s.play_video()
	sleep(self.tlen)
	return False

    def activate(self, x, y):
	pass

class Pause(object):
    def __init__(self, tlen):
	self.tlen=tlen
	self.name='Pause(%f)' % tlen

    def draw(self, time):
	sleep(self.tlen)
	return False

    def activate(self, w, h):
	pass

class Effect2D(object):
    def __init__(self, name, tlen, shader, textures= []):
	self.name= name
	self.model= AttributeBuffer([(-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0)])
	self.model_texture_positions= AttributeBuffer([(-1, -1), (-1, 1), (1, -1), (1, 1)])
	self.vertex_count = self.model.element_count
	self.tlen=tlen
	self.shader=shader
	self.textures=textures

    def activate(self, w, h):
	print 'activating',self.name, self.textures
	self.w=w
	self.h=h
	self.shader.use()
	self.shader.set_resolution(w, h)
	self.textures[0].activate(0)
	self.textures[1].activate(1)
	self.shader.set_tex0(0)
	self.shader.set_tex1(1)
	self.model.attach(self.shader.attr_vposition)
	#self.model_texture_positions.attach(self.shader.aTexturePosition)

    def draw(self, time):
	#glClearColor(0.0, 1.0, 0.0, 1.0)
        #glClear(GL_COLOR_BUFFER_BIT)
	#if time > 2.0:
	#    self.shader.set_tex0(2)

	#self.shader.use()
	#print self.name, 'got time', self.tlen, time
	if time > self.tlen:
	    time = self.tlen

	self.shader.set_time(time)
	self.shader.set_pos(time/self.tlen)

	glDrawArrays(GL_TRIANGLE_STRIP, self.shader.attr_vposition, self.vertex_count)
	return True

    def __str__(self):
	return "Effect2D(%s)" % self.name

    __repr__=__str__

