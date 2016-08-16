'''
Data pipeline:
    Webcam <-> Websocket <-> Python Web <-> WebcamHandler <-> Hawk <-> OpenCV
'''

# Python 2/3 compatibility
from __future__ import print_function

from tornado import websocket, web, ioloop
from threading import Timer
import json
import hawk
import sys, signal

class WebcamHandler(websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WebcamHandler, self).__init__(application, request, **kwargs)
        # fps counter
        self.frames = 0
        self.sum = 0
        # init a object rectangle
        self.rect = {'x':0, 'y':0, 'w':0, 'h':0}
        # repeat timer
        self.timer = None
        # init hawk pipeline
        self.eye = hawk.Eye()

    def open(self):
        print("WebSocket opened")
        self.timer = Timer(1, self.on_timer)
        self.timer.start()

    def on_message(self, message):
        # fps counter
        self.frames += 1
        self.sum += len(message)
        # process data
        rects = self.eye.process(message)
        if (rects is None):
            return
        self.rect['x'], self.rect['y'], self.rect['w'], self.rect['h'] = rects[0].astype(int)
        self.write_message(json.dumps(self.rect))

    def on_close(self):
        print("WebSocket closed")
        self.timer.cancel()

    def on_timer(self):
        if self.frames != 0:
            #print("received: {0} fps, avg. {1} bytes per frame".format(self.frames, self.sum/self.frames))
            pass
        self.frames = 0
        self.sum = 0
        # repeat timer
        self.timer = Timer(1, self.on_timer)
        self.timer.start()

def signal_handler(signal, _):
    print("\nEnd web application")
    ioloop.IOLoop.current().stop()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    app = web.Application([
        (r"/video", WebcamHandler),
        (r"/(.*)", web.StaticFileHandler, {"path": "public"}),
    ])
    app.listen(8888)
    ioloop.IOLoop.current().start()