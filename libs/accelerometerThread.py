import threading


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
            while(not self.record_data):
                values = [0]*3
                for i in range(3):
                    values[i] = self.adc.read_adc(i, gain=GAIN, data_rate=475)
                accel_data.write('{0:32}, {1:20.16}, {2:20.16}, {3:20.16}'.format(time.time(), values[0], values[1], values[2]))
