'''
Hawk identify specified object(s) from frist few frames, then track the target by Adaptive Correlation Filters algorithm. 
Until it lose tracking target, then it would re-identify object(s) again. 
'''
# Python 2/3 compatibility
from __future__ import print_function
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2
import base64
'''
Eye is Hawk's pipeline and central processor.
'''


class Eye:
    def __init__(self):
        self.detector = FaceDetector()
        self.tracker = None

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
        # convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)

        # Check if we have a established tracker
        if self.tracker is None:
            # detect face from frame
            rect = self.detector.detect(gray)
            if rect is not None:
                #print('detected: {0}, {1}'.format(rect, type(rect)))
                self.tracker = MosseTracker(gray, rect)
        else:
            # keep tracking object on incoming frames
            rect = self.tracker.update(gray)
            #print('tracked: {0}, {1}'.format(rect, type(rect)))
            if rect is None:
                self.tracker = None

        if type(rect) is np.ndarray:
            rect = rect.astype(type(int))
        return rect


'''
Face detection using haar cascades
'''


class FaceDetector:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier(
            'model/haarcascade_frontalface_default.xml')

    def detect(self, frame):
        rects = self.cascade.detectMultiScale(
            frame,
            scaleFactor=1.3,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return None
        return rects[0]


''' 
MOSSE tracking - Adaptive Correlation Filters
'''


class MosseTracker:
    def __init__(self, frame, rect):
        self.eps = 1e-5

        x, y, w, h = rect
        self.pos = x, y = x + 0.5 * (w - 1), y + 0.5 * (h - 1)
        self.size = w, h
        img = cv2.getRectSubPix(frame, (w, h), (x, y))

        self.win = cv2.createHanningWindow((w, h), cv2.CV_32F)
        g = np.zeros((h, w), np.float32)
        g[h // 2, w // 2] = 1
        g = cv2.GaussianBlur(g, (-1, -1), 2.0)
        g /= g.max()

        self.G = cv2.dft(g, flags=cv2.DFT_COMPLEX_OUTPUT)
        self.H1 = np.zeros_like(self.G)
        self.H2 = np.zeros_like(self.G)
        for i in xrange(128):
            a = self.preprocess(self.rnd_warp(img))
            A = cv2.dft(a, flags=cv2.DFT_COMPLEX_OUTPUT)
            self.H1 += cv2.mulSpectrums(self.G, A, 0, conjB=True)
            self.H2 += cv2.mulSpectrums(A, A, 0, conjB=True)
        self.update_kernel()
        self.update(frame)

    def update(self, frame, rate=0.125):
        (x, y), (w, h) = self.pos, self.size
        self.last_img = img = cv2.getRectSubPix(frame, (w, h), (x, y))
        img = self.preprocess(img)
        self.last_resp, (dx, dy), self.psr = self.correlate(img)
        self.good = self.psr > 8.0
        if not self.good:
            return None

        self.pos = x + dx, y + dy
        self.last_img = img = cv2.getRectSubPix(frame, (w, h), self.pos)
        img = self.preprocess(img)

        A = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)
        H1 = cv2.mulSpectrums(self.G, A, 0, conjB=True)
        H2 = cv2.mulSpectrums(A, A, 0, conjB=True)
        self.H1 = self.H1 * (1.0 - rate) + H1 * rate
        self.H2 = self.H2 * (1.0 - rate) + H2 * rate
        self.update_kernel()
        return np.array([x - 0.5 * w, y - 0.5 * h, w, h])

    def preprocess(self, img):
        img = np.log(np.float32(img) + 1.0)
        img = (img - img.mean()) / (img.std() + self.eps)
        return img * self.win

    def correlate(self, img):
        C = cv2.mulSpectrums(
            cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT), self.H, 0, conjB=True)
        resp = cv2.idft(C, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
        h, w = resp.shape
        _, mval, _, (mx, my) = cv2.minMaxLoc(resp)
        side_resp = resp.copy()
        cv2.rectangle(side_resp, (mx - 5, my - 5), (mx + 5, my + 5), 0, -1)
        smean, sstd = side_resp.mean(), side_resp.std()
        psr = (mval - smean) / (sstd + self.eps)
        return resp, (mx - w // 2, my - h // 2), psr

    def update_kernel(self):
        self.H = self.divSpec(self.H1, self.H2)
        self.H[..., 1] *= -1

    def rnd_warp(self, img):
        h, w = img.shape[:2]
        T = np.zeros((2, 3))
        coef = 0.2
        ang = (np.random.rand() - 0.5) * coef
        c, s = np.cos(ang), np.sin(ang)
        T[:2, :2] = [[c, -s], [s, c]]
        T[:2, :2] += (np.random.rand(2, 2) - 0.5) * coef
        c = (w / 2, h / 2)
        T[:, 2] = c - np.dot(T[:2, :2], c)
        return cv2.warpAffine(img, T, (w, h), borderMode=cv2.BORDER_REFLECT)

    def divSpec(self, A, B):
        Ar, Ai = A[..., 0], A[..., 1]
        Br, Bi = B[..., 0], B[..., 1]
        C = (Ar + 1j * Ai) / (Br + 1j * Bi)
        C = np.dstack([np.real(C), np.imag(C)]).copy()
        return C
