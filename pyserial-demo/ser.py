#!/usr/bin/env python3
import serial

def main():
    ser = serial.Serial("/dev/ttyftdi")
    ser.baudrate = 9600
    ser.write("abcdefghijklmnopqrstuvwxyz");
    ser.close()

if __name__ == "__main__":
    main()
