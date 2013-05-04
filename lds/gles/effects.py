#
# encoding: utf-8
#
from shortcrust.shader import ShaderProgram
from shortcrust.buffer import AttributeBuffer
from shortcrust.gl2 import *
from time import sleep

class Pause(object):
    def __init__(self, tlen):
	self.tlen=tlen
	self.name='Pause(%f)' % tlen

    def draw(self, time):
	sleep(self.tlen)

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

	self.textures[0].activate(0)
	self.textures[1].activate(1)

	self.shader.use()
	self.shader.set_resolution(w, h)

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

	self.shader.set_time(time)
	self.shader.set_pos(0.1+time/self.tlen)

	glDrawArrays(GL_TRIANGLE_STRIP, self.shader.attr_vposition, self.vertex_count)
