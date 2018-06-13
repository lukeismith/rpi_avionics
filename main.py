# Main control loop
# Zero g point of ADXL377 is Vcc/2
# 0.025 uF cap on each output pin for 200Hz bandwidth
# 6.5 mV/g on each channel

import time
import threading
import Adafruit_ADS1x15
import gpiozero



# Initialize adc module
adc = Adafruit_ADS1x15.ADS1115()
# Keep recording until this is set to false
record_data = threading.Event()


class accelerometerThread(threading.Thread):
    def __init__(self, adc, record_data):
        threading.Thread.__init__(self)
        self.adc = adc
        self.record_data = record_data
    
    def run(self):
        # Continuously record adc values to file
        GAIN = 1
        with open ("data/accelerometer.txt", "a+") as accel_data:
            accel_data.write('{0:32}, {1:20}, {2:20}, {3:20}'.format("Time", "X-Axis", "Y-Axis", "Z-Axis"))
            while(self.record_data):
                values = [0]*4
                for i in range(4):
                    values[i] = self.adc.read_adc(i, gain=GAIN, data_rate=475)
                accel_data.write('{0:32}, {1:20.16}, {2:20.16}, {3:20.16}'.format(time.time(), values[0], values[1], values[2]))

status_led = gpiozero.LED(23)
record_switch = gpiozero.Button(24)

record_data.set() # allows threads to work

xyzs = accelerometerThread(adc, record_data)
xyzs.run()

while True:

    if not record_switch.is_pressed:
        record_data.clear()

    if record_data:
        status_led.on()

    sleep(0.5) # Don't waste too much cpu resources
