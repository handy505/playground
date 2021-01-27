#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime
import serial


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


def main():
    print('Modbus Master Simulator')
    ser = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=0.8)

    lines = [ '3d 03 00 00 00 02 c1 37',
              '3e 03 00 00 00 02 c1 04', 
              '00 00 00 00 00 02 c1 04', 
              '01 03 c0 20 00 13 39 cd',
              '01 03 c0 00 00 02 f8 0b', 
              '01 03 c0 10 00 02 f9 ce',
              '00 00 00 00 00 02 f9 ce',
              '02 03 c0 20 00 13 39 fe',
              '02 03 c0 00 00 02 f8 38',
              '02 03 c0 10 00 02 f9 fd',
              '00 00 00 00 00 02 f9 fd']

    while True:
        for line in lines:
            print('[32mMaster: {}[m'.format(line))
            txpacket = bytearray.fromhex(line)
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
