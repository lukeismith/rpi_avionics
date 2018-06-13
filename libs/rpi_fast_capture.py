import cv2
import numpy as np
import subprocess as sp
import time
import atexit
import threading

class rpi_fast_capture(threading.Thread):


    def __init__(self, record_data):
        threading.Thread.__init__(self)
        self.record_data = record_data
        self.frames1 = []   #frame buffer
        self.frames2 = []
        self.max_frames = 300 #frames allowed in each buffer
        self.N_frames1 = 0
        self.N_frames2 = 0
        self.(w,h) = (640, 480)
        self.bytesPerFrame = self.w * self.h
        self.fps = 60 # intentionally set this at about half max to free cpu resources
        self.videoCmd = split.("raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview")
        self.cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE)
        atexit.register(cameraProcess.terminate)

    def run():
        

    def record():



    def save():