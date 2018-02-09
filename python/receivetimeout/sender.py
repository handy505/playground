#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import serial


class MainThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        ser = serial.Serial(port='/dev/ttyUSB2', baudrate=9600, timeout=0.8)

        while True:
            n = ser.in_waiting
            if n:
                print(time.time())
                p = self.receiving_until_timeout(ser, 0.1)
                print('{}'.format(p))
                print(time.time())


    def receiving_until_timeout(self, sp, timeout):
        num = sp.in_waiting
        rtime = time.time()
        while time.time() - rtime < timeout:
            if sp.in_waiting != num:
                num = sp.in_waiting
                rtime = time.time()
        return sp.read(sp.in_waiting)

        
def main():

    ser = serial.Serial(port='/dev/ttyUSB2', baudrate=9600, timeout=0.8)

    SEND_INTERVAL = 0.8
    num = 1234
    bs = str(num).encode('utf-8')
    ser.write(bs)
    ser.flush()
    while ser.out_waiting:
        pass
    time.sleep(SEND_INTERVAL)

    num += 1
    bs = str(num).encode('utf-8')
    ser.write(bs)
    ser.flush()
    while ser.out_waiting:
        pass
    time.sleep(SEND_INTERVAL)

    num += 1
    bs = str(num).encode('utf-8')
    ser.write(bs)
    ser.flush()
    while ser.out_waiting:
        pass
    time.sleep(SEND_INTERVAL)

    num += 1
    bs = str(num).encode('utf-8')
    ser.write(bs)
    ser.flush()
    while ser.out_waiting:
        pass
    time.sleep(SEND_INTERVAL)





if __name__ == "__main__":
    main()

