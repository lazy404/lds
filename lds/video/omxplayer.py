import subprocess, threading, time, select


class OmxPlayerThread(threading.Thread):
    def __init__(self, video, x1, y1, x2, y2):
        threading.Thread.__init__(self)
        self.video=video
        self.lready=threading.Lock()
        self.lgo=threading.Lock()
        self.lgo.acquire()
        self.lready.acquire()
	if x1 + y1 +x2 + y2 > 0:
	    self.opts=['--win', '%d %d %d %d' % (x1,y1,x2,y2)]
	else:
	    self.opts=[]

    def get_queue(self):
        return self.inq

    def end(self):
        self.active=False

    def play_video(self):
        if self.lgo.locked():
            self.lgo.release()
            return True
        return False

    def wait_ready(self):
        if self.lready.locked():
            self.lready.acquire()
        return True

    def run(self):
	
        p=subprocess.Popen(['/usr/src/omxplayer/omxplayer.bin','-p'] + self.opts + [self.video], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, env={'LD_LIBRARY_PATH':'/opt/vc/lib:/usr/src/omxplayer/ffmpeg_compiled/usr/local/lib/:/usr/lib/omxplayer'})

        epoll = select.epoll()
        epoll.register(p.stdout.fileno(), select.EPOLLIN)
        events = epoll.poll(100)

        print p.stdout.readline()
        self.lready.release()

        self.lgo.acquire()

        p.stdin.write('g')
        p.stdin.flush()

        events = epoll.poll(20)
        self.lready.release()
        print p.stdout.readlines()

        p.wait()

if __name__ == '__main__':
    x=time.time()
    s=OmxPlayerThread('/usr/src/test.h264', 0, 1536, 1080, 1920)
    s.start()
    s.wait_ready()
    y=time.time()
    print 'load time',y-x

    s.play_video()
    x=time.time()

    s.wait_ready()
    y=time.time()
    print 'play time',y-x
