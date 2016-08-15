from tornado import websocket, web, ioloop
from threading import Timer
import random
import json

class WebcamHandler(websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WebcamHandler, self).__init__(application, request, **kwargs)
        # output frame counter
        self.frames = 0
        self.sum = 0
        # init a object rectangle
        self.rect = {'x':0, 'y':0, 'w':0, 'h':0}
        # repeat timer
        self.timer = None

    def open(self):
        print("WebSocket opened")
        self.timer = Timer(1, self.on_timer)
        self.timer.start()

    def on_message(self, message):
        #self.write_message(u"You said: " + message)
        self.frames += 1
        self.sum += len(message)

    def on_close(self):
        print("WebSocket closed")
        self.timer.cancel()

    def on_timer(self):
        if self.frames == 0:
            return
        print "received: {0} fps, avg. {1} bytes per frame".format(self.frames, self.sum/self.frames)
        self.frames = 0
        self.sum = 0

        # simulate object identification
        self.rect['x'] = random.randint(0, 200)
        self.rect['y'] = random.randint(0, 100)
        self.rect['w'] = random.randint(50, 100)
        self.rect['h'] = random.randint(50, 100)

        self.write_message(json.dumps(self.rect))
        
        # repeat timer
        self.timer = Timer(1, self.on_timer)
        self.timer.start()

if __name__ == "__main__":
    app = web.Application([
        (r"/video", WebcamHandler),
        (r"/(.*)", web.StaticFileHandler, {"path": "public"}),
    ])
    app.listen(8888)
    ioloop.IOLoop.current().start()