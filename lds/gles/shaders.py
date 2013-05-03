from shortcrust.shader import ShaderProgram
from shortcrust.buffer import AttributeBuffer
from shortcrust.gl2 import *

class TexShader(ShaderProgram):
	# A 'do nothing' vertex shader that simply passes vertex positions through to screen coordinates.
	vertex_shader = """
		attribute vec4 vPosition;
		//attribute vec2 aTexturePosition;

                varying vec2 vTextureCoord;

		void main()
		{
			gl_Position = vPosition;
			//vTextureCoord = aTexturePosition;
		}
	"""

	# A fragment shader that colours pixels as a function of x/y coordinate, resolution and time.
	fragment_shader = """
#ifdef GLES2
		precision mediump float;
#endif
                varying vec2 vTextureCoord;

		uniform float time;
		uniform float pos;
		uniform vec2 resolution;

		uniform sampler2D tex0;
		uniform sampler2D tex1;

		void main( void ) {

			vec2 position = ( gl_FragCoord.xy / resolution.xy );

			//if ( time < 2.0)
			//    gl_FragColor = texture2D(tex0, position);
			//else 
			//    gl_FragColor = texture2D(tex1, position);

			gl_FragColor = mix(texture2D(tex0, position), texture2D(tex1, position), pos);

		}
	"""

	def __init__(self):
		super(TexShader, self).__init__()

		# Retrieve the locations of the position, time and resolution attributes / uniforms
		# so that we can push values to them later
		self.attr_vposition = self.get_attrib('vPosition')
		#self.aTexturePosition = self.get_attrib('aTexturePosition')

		self.unif_time = self.get_uniform('time')
		self.unif_pos = self.get_uniform('pos')

		self.unif_resolution = self.get_uniform('resolution')

		self.utex0 = self.get_uniform('tex0')
		self.utex1 = self.get_uniform('tex1')

	def set_tex0(self, value):
		glUniform1i(self.utex0, value)

	def set_tex1(self, value):
		glUniform1i(self.utex1, value)
	
	def set_time(self, value):
		"""
			Set the 'time' uniform within the shader
		"""
		glUniform1f(self.unif_time, value)
	def set_pos(self, value):
		"""
			Set the 'time' uniform within the shader
		"""
		glUniform1f(self.unif_pos, value)

	def set_resolution(self, width, height):
		"""
			Set the 'resolution' uniform from the passed width and height
		"""
		glUniform2f(self.unif_resolution, width, height)

class PlasmaShader2(TexShader):
	fragment_shader = """
		uniform float time;
		uniform vec2 resolution;

		void main( void ) {

			vec2 position = ( gl_FragCoord.xy / resolution.xy );

			float color = 0.0;
			color += sin( position.x * cos( time / 15.0 ) * 80.0 ) + cos( position.y * cos( time / 15.0 ) * 10.0 );
			color += sin( position.y * sin( time / 10.0 ) * 40.0 ) + cos( position.x * sin( time / 25.0 ) * 40.0 );
			color += sin( position.x * sin( time / 5.0 ) * 10.0 ) + sin( position.y * sin( time / 35.0 ) * 80.0 );
			color *= sin( time / 10.0 ) * 0.5;

			gl_FragColor = vec4( vec3( color*0.5, color, sin( color + time / 3.0 ) * 0.75 ), 1.0 );

		}
	"""


if __name__ == '__main__':
    from shortcrust.raspi.egl import EGL
    egl = EGL()
    s=PlasmaShader()
    s.use()
    print s
