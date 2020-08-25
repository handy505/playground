#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime
import serial

ser = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=0.8)


def hexdump(src, length=16):
    '''
    reference to http://code.activestate.com/recipes/142812-hex-dumper/
    modity python2 to python3
    '''
    result = []
    digits = 4 if isinstance(src, bytes) else 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(['{:>02X}'.format(x) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        line = '{:>04} {:<48s} {}'.format(i, hexa, text)
        result.append(line) 
    return '\n'.join(result)


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
            print(hexdump(rxpacket))

            time.sleep(1)


if __name__ == '__main__':

    main()
