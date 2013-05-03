#
# encoding: utf-8
#
from shortcrust.shader import ShaderProgram
from shortcrust.buffer import AttributeBuffer
from shortcrust.gl2 import *

class Effect2D(object):
    def __init__(self, name, w ,h, tlen, shader, textures= []):
	self.name= name
	self.model= AttributeBuffer([(-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0)])
	self.vertex_count = self.model.element_count
	self.tlen=tlen
	self.shader=shader
	self.textures=textures

    def activate(self, w, h):
	self.w=w
	self.h=h
	self.shader.use()
	self.shader.set_resolution(w, h)
        glViewport(0, 0, w, h)
	self.model.attach(self.shader.attr_vposition)

    def draw(self, time):
	#glClearColor(0.0, 1.0, 0.0, 1.0)
        #glClear(GL_COLOR_BUFFER_BIT)

	#self.shader.use()
	self.shader.set_time(time)

	glDrawArrays(GL_TRIANGLE_STRIP, self.shader.attr_vposition, self.vertex_count)
