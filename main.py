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

from picamera import PiCamera
from libs.Adafruit_GPIO import PWM
from libs.Adafruit_BME280 import BME280
from libs import Adafruit_ADS1x15
from libs.accelerometerThread import accelerometerThread
from libs.bnoThread import bnoThread
from libs.Adafruit_BNO055 import BNO055
#from libs.cameraThread import cameraThread

def main():
    # Initialize adc module
    #adc = Adafruit_ADS1x15.ADS1115()
    
    # Keep recording until this is set to true
    #record_data = threading.Event()
    # Initialize gpio pins
    #status_led = gpiozero.LED(23)
    #record_switch = gpiozero.Button(24)

    # Initialize SPI device
    # 
    #sense_pressure = gpiozero.SPIDevice()

    #xyzs = accelerometerThread(adc, record_data)
    #cam = cameraThread(record_data)

    #bno = bnoThread(record_data)

    #bno.start()

    #xyzs.start()
    #cam.start()
    '''
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1

    with open ("data/200g.txt", "a+") as adc_data:
        adc_data.write('{0:32}, {1:20}, {2:20}, {3:20}\n'.format("TIME", 'x', 'y', 'z'))

        while True:
            x = adc.read_adc_difference(1, gain=GAIN, data_rate=860)
            y = adc.read_adc_difference(2, gain=GAIN, data_rate=860)
            z = adc.read_adc_difference(3, gain=GAIN, data_rate=860)
            adc_data.write('{0:32}, {1:20}, {2:20}, {3:20}\n'.format(time.time(), x, y, z))

        
    
    bno = BNO055.BNO055()
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    with open ("data/bno.txt", "a+") as bno_data:
        bno_data.write("Using format: {0}".format("hello"))
        bno_data.write('{0:32}, {1:20}, {2:20}, {3:20}, {4:20}, {5:20}, {6:20}, {7:20}, {8:20}, {9:20}\n'.format("Time", "Mag X", "Mag Y", "Mag Z", "Gyro X", "Gyro Y", "Gyro Z", "Accel X", "Accel Y", "Accel Z"))

        while True:
            mag = bno.read_magnetometer()
            gyro = bno.read_gyroscope()
            accel = bno.read_accelerometer()
            bno_data.write('{0:32}, {1:20.16}, {2:20.16}, {3:20.16}, {4:20.16}, {5:20.16}, {6:20.16}, {7:20.16}, {8:20.16}, {9:20.16}\n'.format(time.time(), mag[0], mag[1], mag[2], gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2]))
    '''
    #Try both adc and BNO055 at the same time

    status = PWM()

    bar = BME280() #I changed the address in the library and filter/oversampling are already off/set to 1

    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1
    bno = BNO055.BNO055()
    bno.begin()
    with open ("data/200g.txt", "a+") as adc_data, open ("data/bno.txt", "a+") as bno_data, open ("data/bmp280.txt", "a+") as bmp_data:
        adc_data.write('{0:32}, {1:20}, {2:20}, {3:20}, {4:20}\n'.format("TIME", 'voltage', 'x', 'y', 'z'))
        bno_data.write('{0:32}, {1:32}, {2:32}, {3:32}, {4:32}, {5:32}, {6:32}, {7:32}, {8:32}, {9:32}\n'.format("Time", "Mag X", "Mag Y", "Mag Z", "Gyro X", "Gyro Y", "Gyro Z", "Accel X", "Accel Y", "Accel Z"))
        bmp_data.write('{0:32}, {1:32}\n'.format("Time", "Pressure (Pa)"))
        status.start(18, 500, .5)

        count = 0
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
                pressure = bar.read_pressure()
                bmp_data.write('{0:32}, {1:32}\n'.format(time.time(), pressure))
                count = 0
            else:
                count += 1

    '''
    while True:

        if record_switch.is_pressed:
            record_data.set() # Sets event to true to signal threads to stop

        if not record_data:
            status_led.on()

        time.sleep(0.5) # Don't waste too much cpu resources
    '''

if __name__ == "__main__":
    main()
