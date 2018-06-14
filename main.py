# Main control loop
# Zero g point of ADXL377 is Vcc/2
# 0.025 uF cap on each output pin for 200Hz bandwidth
# 6.5 mV/g on each channel

import time
import threading
import Adafruit_ADS1x15
import gpiozero
from picamera import PiCamera
from libs.accelerometerThread import accelerometerThread
from libs.cameraThread import cameraThread

def main():
    # Initialize adc module
    adc = Adafruit_ADS1x15.ADS1115()
    # Keep recording until this is set to true
    record_data = threading.Event()
    # Initialize gpio pins
    status_led = gpiozero.LED(23)
    record_switch = gpiozero.Button(24)

    xyzs = accelerometerThread(adc, record_data)
    cam = cameraThread(record_data)

    xyzs.start()
    cam.start()

    while True:

        if not record_switch.is_pressed:
            record_data.set() # Sets event to true to signal threads to stop

        if not record_data:
            status_led.on()

        time.sleep(0.5) # Don't waste too much cpu resources


if __name__ == "__main__":
    main()
