#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime
import serial

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.8)

def load():
    lines = []
    with open('config.txt', 'r', encoding='utf-8') as fr:
        for i, line in enumerate(fr.readlines()):
            s = line.strip()
            t = (i, s)
            lines.append(t)
    return lines

def main():
    print('IPV Box Simulator')

    lines = load()

    while True:
        for line in lines:
            print('[#{}] {}'.format(line[0], line[1]))
            txpacket = bytearray.fromhex(line[1])

            ser.reset_output_buffer()
            ser.reset_input_buffer()
            ser.write(txpacket)
            ser.flush()
            time.sleep(0.2) # wait for machine processing 
            time.sleep(1) # force wait
            rxpacket = ser.read(ser.in_waiting)
            print(' '.join(['{:02x}'.format(b) for b in rxpacket]))

            time.sleep(1)


if __name__ == '__main__':

    main()
