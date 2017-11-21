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
        ser = serial.Serial(port='/dev/ttyUSB3', baudrate=9600, timeout=0.8)

        while True:
            time.sleep(1)
            n = ser.in_waiting
            if n:
                t0 = time.time()
                p = self.receiving_until_timeout(ser, 0.1)
                t1 = time.time()
                print('{}'.format(p))
                print('{} -> {}, {}'.format(t0, t1, t1-t0))


    def receiving_until_timeout(self, sp, timeout):
        num = sp.in_waiting
        rtime = time.time()
        while time.time() - rtime < timeout:
            if sp.in_waiting != num:
                num = sp.in_waiting
                rtime = time.time()
        return sp.read(sp.in_waiting)

        
def main():
    m = MainThread()
    m.start()

if __name__ == "__main__":
    main()

