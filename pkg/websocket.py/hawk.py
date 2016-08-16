'''
Hawk identify specified object(s) from frist few frames, then track the target by Adaptive Correlation Filters algorithm. 
Until it lose tracking target, then it would re-identify object(s) again. 
'''
# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import base64

'''
Face detection using haar cascades
'''
class FaceDetector:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)

        rects = self.cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, 
                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return None
        return rects

'''
Eye is Hawk's pipeline and central processor.
'''
class Eye:
    def __init__(self):
        self.detector = FaceDetector()
    
    def process(self, b64):
        '''
        RGBA (~300K) -> PNG (~160K) -> Base64 -> Bytes -> Frame (RGB) -> Target rectangle
        Less bandwidth than raw array tranmission
        '''
        # decode base64 to bytes array
        _bytes = base64.b64decode(b64.split(",")[1])
        # use numpy to construct an array from the bytes
        _matrix = np.fromstring(_bytes, dtype='uint8')
        # decode the array into an image
        frame = cv2.imdecode(_matrix, cv2.IMREAD_UNCHANGED)
        # detect face from frame
        rects = self.detector.detect(frame)
        return rects

