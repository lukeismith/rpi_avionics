import threading
import picamera as PiCamera

class cameraThread(threading.Thread):
    
    def __init__(self, record_data)
    threading.Thread.__init__(self)
    self.record_data = record_data

    def run(self):
        with PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 60
            camera.start_recording("video/capture.h264")
            record_data.wait()
            camera.stop_recording()