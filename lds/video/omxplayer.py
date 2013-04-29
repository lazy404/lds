import subprocess, threading, time


class OmxPlayerThread(threading.Thread):
    def __init__(self, video):
        threading.Thread.__init__(self)
	self.video=video

    def get_queue(self):
        return self.inq

    def end(self):
        self.active=False


    def run(self):
	print time.time()
	p=subprocess.Popen(['/usr/bin/omxplayer', self.video], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	print time.time()
	p.poll()
	print time.time()

	s=time.time()
	print p.communicate()
	p.wait()
	print (time.time()*1000-s*1000)/1000

if __name__ == '__main__':
    s=OmxPlayerThread('/usr/src/test.h264')
    s.run()