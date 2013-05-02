#from pyopengles import *
from shortcrust.gl2 import *
import pygame
import sys

class Texture(Object):
    def __init__(self, filename, format=GL_RGB):
	self.format=format
	self.filename=filename
	self.data_ready=False
	self.texture_ready=False

    def load_data(self):
	try:
    	    print "loading", filename

	    self.texture_id=glGenTextures(1)

    	    tmp = pygame.image.load(filename)
	
	    if self.format == GL_RGB:
    		self.data = pygame.image.tostring(tmp, "RGB", 1)
	    elif self.format == GL_RGBA:
    		self.data = pygame.image.tostring(tmp, "RGBA", 1)
	    else:
		self.data = pygame.image.tostring(tmp, "RGB", 1)

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
    	    glBindTexture(GL_TEXTURE_2D, self.texture_id)
    	    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
    	    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
    	    glTexImage2D(GL_TEXTURE_2D, 0, self.format, self.w, self.h, 0, self.format, GL_UNSIGNED_BYTE, self.data)
	    self.texture_ready=True
	except Exception, e:
	    print self, 'error in activate', e
	    raise e

    def activate(self, glid):
	try:
	    if not self.texture_ready:
		self.load_texture()

	    glActiveTexture(GL_TEXTURE0+glid)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
	    self.glid=glid
	except Exception, e:
	    print self, 'error in activate', e

    def unload(self):
    	glDeleteTextures(self.texture_id)
	self.glid=-1
	self.texture_ready=False

if __name__ == '__main__':
    t1=Texture('tex1.png')
    t2=Texture('tex2.png')
