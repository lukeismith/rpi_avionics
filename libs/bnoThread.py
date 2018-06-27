
import logging
import sys
import time
import threading

from Adafruit_BNO055 import BNO055


class bnoThread(threading.Thread):
    def __init(self, mode, record_data):
        threading.Thread.__init__(self)
        self.bno = BNO055.BNO055(serial_port='/dev/serial10', rst=18)
        self.record_data = record_data
        self.mode = mode

    def run(self):
        if not self.bno.begin():
            print("Well shiieeettttt")
        with open ("data/bno.txt", "a+") as bno_data:
            bno_data.write("Using format: {0}".format(self.mode))
            bno_data.write('{0:32}, {1:20}, {2:20}, {3:20}, {4:20}, {5:20}, {6:20}, {7:20}, {8:20}, {9:20}'.format("Time", "Mag X", "Mag Y", "Mag Z", "Gyro X", "Gyro Y", "Gyro Z", "Accel X", "Accel Y", "Accel Z"))

            while(not self.record_data):
                mag = self.bno.read_magnetometer();
                gyro = self.bno.read_gyroscope();
                accel = self.bno.read_accelerometer();
                bno_data.write('{0:32}, {1:20.16}, {2:20.16}, {3:20.16}, {4:20.16}, {5:20.16}, {6:20.16}, {7:20.16}, {8:20.16}, {9:20.16}'.format(time.time(), mag[0], mag[1], mag[2], gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2]))
