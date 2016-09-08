#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial

def main():
    ser = serial.Serial("/dev/ttyftdi")
    ser.baudrate = 9600
    ser.write("abcdefghijklmnopqrstuvwxyz".encode());
    ser.close()

if __name__ == "__main__":
    main()
