#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import RPi.GPIO as GPIO

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    chan_out_list = [29, 31, 36, 38, 40, 33, 37]
    GPIO.setup(chan_out_list, GPIO.OUT)
    chan_in_list = [22, 32]
    GPIO.setup(chan_in_list, GPIO.IN)

    GPIO.output(33, GPIO.HIGH)

    p = GPIO.PWM(37, 100)
    p.start(50)
    print("press any key to exit")
    i = input()
    p.stop()
    GPIO.cleanup()


if __name__ == "__main__":

    print("jig-pwm")
    main()
