
import threading
import time
import serial
import queue

import random




class Collector(threading.Thread):
    def __init__(self, ser_name, pipeline):
        threading.Thread.__init__(self)
        self.pipeline = pipeline
        self.ser_name = ser_name
        try:
            self.ser = serial.Serial(port=ser_name, baudrate=9600, timeout=0.8)
        except Exception as err:
            print(err)

    def run(self):
        while True:
            value = random.randint(0, 10)
            print('collect data from {}, data: {}'.format(self.ser_name, value))
            self.pipeline.put(value)
            time.sleep(1)


class MainThread(threading.Thread):
    def __init__(self, pipeline1, pipeline2):
        threading.Thread.__init__(self)
        self.pipeline1 = pipeline1 
        self.pipeline2 = pipeline2 

    def run(self):
        while True:
           v1 = self.pipeline1.get() 
           v2 = self.pipeline2.get() 
           print('main concat {} and {}, then plot'.format(v1, v2))
           time.sleep(2)






def main():

    q1 = queue.Queue()
    q2 = queue.Queue()

    c1 = Collector('/dev/ttyUSB0', q1)
    c2 = Collector('/dev/ttyUSB1', q2)


    m = MainThread(q1, q2)




    c1.start()
    c2.start()
    m.start()

if __name__ == '__main__':
    main()
