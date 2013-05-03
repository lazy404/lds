#from pyopengles import *
from shortcrust.gl2 import *
from pygame import image
import sys

class Texture(object):
    def __init__(self, filename, format=GL_RGB):
	self.format=format
	self.filename=filename
	self.data_ready=False
	self.texture_ready=False
	self.texture_id=-1
	self.texture_index=-1

    def load_data(self):
	try:
	    print 'load_data', str(self)
	    if self.data_ready:
		print 'already loaded'
		return

	    self.texture_id=glGenTextures(1)

    	    tmp = image.load(self.filename)
	
	    if self.format == GL_RGB:
    		self.data = image.tostring(tmp, "RGB", 1)
	    elif self.format == GL_RGBA:
    		self.data = image.tostring(tmp, "RGBA", 1)
	    else:
		self.data = image.tostring(tmp, "RGB", 1)

    	    self.w = tmp.get_width()
    	    self.h = tmp.get_height()
	    del tmp

	    self.data_ready=True

	except Exception,e:
	    print self, 'error in load_data', e
	    raise e

    def load_texture(self):
	try:
	    if not self.data_ready:
		self.load_data()
	    print 'load texture', str(self)
    	    glBindTexture(GL_TEXTURE_2D, self.texture_id)
	    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    	    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
    	    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
    	    glTexImage2D(GL_TEXTURE_2D, 0, self.format, self.w, self.h, 0, self.format, GL_UNSIGNED_BYTE, self.data)
	    self.texture_ready=True
	except Exception, e:
	    print self, 'error in activate', e
	    raise e

    def activate(self, texture_index):
	try:
	    if not self.texture_ready:
		self.load_texture()

	    glActiveTexture(GL_TEXTURE0 + texture_index)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
	    self.texture_index=texture_index
	    print 'activated texture %s (%dx%d) %d as %d' % (self.filename, self.w, self.h, self.texture_id, self.texture_index)

	except Exception, e:
	    print self, 'error in activate', e

    def unload(self):
    	glDeleteTextures(self.texture_id)
	self.texture_index=-1
	self.texture_ready=False

    def __str__(self):
	return 'Texture(%s) %d as %d' % (self.filename, self.texture_id, self.texture_index)

    def __repr__(self):
	return str(self)

if __name__ == '__main__':
    from shortcrust.raspi.egl import EGL

    egl = EGL()
    t1=Texture('tex1.png')
    t2=Texture('tex2.png')
    t1.activate(1)

    t2.activate(0)
