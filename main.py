# Main control loop
# Zero g point of ADXL377 is Vcc/2
# ADXL377 vcc max is 3.6V
# 0.025 uF cap on each output pin for 200Hz bandwidth
# 6.5 mV/g on each channel

import time
import threading
import gpiozero
import logging
import sys
import importlib
import RPi.GPIO as IO

from picamera import PiCamera
from libs.Adafruit_BME280 import BME280
from libs import Adafruit_ADS1x15
from libs.accelerometerThread import accelerometerThread
from libs.bnoThread import bnoThread
from libs.Adafruit_BNO055 import BNO055
#from libs.cameraThread import cameraThread

def main():

    IO.setmode(IO.BCM)
    IO.setup(18, IO.OUT)

    bar = BME280() #I changed the address in the library and filter/oversampling are already off/set to 1

    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1
    bno = BNO055.BNO055()
    bno.begin()
    with open ("data/200g.txt", "a+") as adc_data, open ("data/bno.txt", "a+") as bno_data, open ("data/bmp280.txt", "a+") as bmp_data:
        adc_data.write('{0:32}, {1:20}, {2:20}, {3:20}, {4:20}\n'.format("TIME", 'voltage', 'x', 'y', 'z'))
        bno_data.write('{0:32}, {1:32}, {2:32}, {3:32}, {4:32}, {5:32}, {6:32}, {7:32}, {8:32}, {9:32}\n'.format("Time", "Mag X", "Mag Y", "Mag Z", "Gyro X", "Gyro Y", "Gyro Z", "Accel X", "Accel Y", "Accel Z"))
        bmp_data.write('{0:32}, {1:32}\n'.format("Time", "Pressure (Pa)"))

        count = 0
        count2 = 0
        while True:
            v = adc.read_adc(0, gain=GAIN, data_rate=860)
            x = adc.read_adc(1, gain=GAIN, data_rate=860)
            y = adc.read_adc(2, gain=GAIN, data_rate=860)
            z = adc.read_adc(3, gain=GAIN, data_rate=860)
            mag = bno.read_magnetometer()
            gyro = bno.read_gyroscope()
            accel = bno.read_accelerometer()
            adc_data.write('{0:32}, {1:20}, {2:20}, {3:20}, {4:20}\n'.format(time.time(), v, x, y, z))
            bno_data.write('{0:32}, {1:32}, {2:32}, {3:32}, {4:32}, {5:32}, {6:32}, {7:32}, {8:32}, {9:32}\n'.format(time.time(), mag[0], mag[1], mag[2], gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2]))
            if (count == 7):
                IO.output(18, 0)
                count2 += 1
                pressure = bar.read_pressure()
                bmp_data.write('{0:32}, {1:32}\n'.format(time.time(), pressure))
                count = 0
            else:
                count += 1
            if (count2 == 5):
                IO.output(18, 1)
                count2 = 0

if __name__ == "__main__":
    main()
