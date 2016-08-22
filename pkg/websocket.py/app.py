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
    timer = None

    def __init__(self, application, request, **kwargs):
        super(WebcamHandler, self).__init__(application, request, **kwargs)
        # fps counter
        self.frames = 0
        self.sum = 0
        # init a object rectangle
        self.rect = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
        # repeat timer
        self.timer = None
        # init hawk pipeline
        self.eye = hawk.Eye()

    def open(self):
        print("WebSocket opened")
        WebcamHandler.timer = Timer(1, self.on_timer)
        WebcamHandler.timer.start()

    def on_message(self, message):
        # fps counter
        self.frames += 1
        self.sum += len(message)
        # process data
        rect = self.eye.process(message)
        if (rect is None):
            return
        self.rect['x'], self.rect['y'], self.rect['w'], self.rect['h'] = rect
        self.write_message(json.dumps(self.rect))

    def on_close(self):
        print("WebSocket closed")
        WebcamHandler.timer.cancel()

    def on_timer(self):
        if self.frames != 0:
            #print("received: {0} fps, avg. {1} bytes per frame".format(self.frames, self.sum/self.frames))
            pass
        self.frames = 0
        self.sum = 0
        # repeat timer
        WebcamHandler.timer = Timer(1, self.on_timer)
        WebcamHandler.timer.start()


def signal_handler(signal, _):
    if WebcamHandler.timer is not None:
        WebcamHandler.timer.cancel()
    ioloop.IOLoop.current().stop()
    ioloop.IOLoop.current().close()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    app = web.Application([
        (r"/video", WebcamHandler),
        (r"/(.*)", web.StaticFileHandler, {"path": "public",
                                           "default_filename": "index.html"}),
    ])
    app.listen(8888)
    ioloop.IOLoop.current().start()
