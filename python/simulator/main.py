#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

class Inverter(object):
    def __init__(self, id):
        self.id = id
        self.alarm = 0x00000000
        self.error = 0x00000000
        self.reflash_timestamp = time.time()
        self.TotalOutputPower = 0

    def __str__(self):
        return 'Inverter-{}, {} KW, {} KWH'.format(
            self.id, 
            round(self.OutputPower/1000,3), 
            round(self.TotalOutputPower/1000,3))

    def reflash(self):
        diff = time.time() - self.reflash_timestamp
        self.OutputPower = (5000/3600)*diff
        self.TotalOutputPower += self.OutputPower


def main():
    inv = Inverter(1)



    for _ in range(1, 10):
        inv.reflash()
        print(inv)
        time.sleep(1)


if __name__ == '__main__':

    main()
