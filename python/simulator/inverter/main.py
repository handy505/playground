#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime

import crc
import memorymapping
import concatenate
import devices


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.invgroup = []
        for id in range(1, 3):
            inv = devices.Inverter(id)
            print(inv)
            self.invgroup.append(inv)

        self.imeter = devices.DCBoxIlluMeter(11)
        self.tmeter = devices.DCBoxTempMeter(10)
            
        self.concatthread = concatenate.ConcatThread(self.invgroup, self.imeter, self.tmeter)

    def run(self):

        refresh_timestamp = time.time()

        self.concatthread.start()
        while True:
            now = time.time()
            if now - refresh_timestamp > 3:
                for inv in self.invgroup:
                    inv.refresh()

                self.imeter.refresh()
                self.tmeter.refresh()

                #dt = datetime.datetime.fromtimestamp(now)
                #print('Refresh at {}'.format(dt))
                refresh_timestamp = now


def main():
    print('PV Inverter simulator')
    mainthread = MainThread()
    mainthread.start()


def demo():

    inv = Inverter(1)
    imeter = DCBoxIlluMeter(10)
    tmeter = DCBoxTempMeter(11)

    group = [inv, imeter, tmeter]


    #q = '01 03 c0 31 00 02'
    q = '0a 03 00 19 00 01'
    q = bytearray.fromhex(q)
    q = crc.append_crc16(q)
    #print('query: {}'.format(q))

    [dev.refresh() for dev in group]

    for dev in group:
        r = dev.read_memory_by_jbus(q)
        if r:
            s = ' '.join(['{:02x}'.format(b) for b in r])
            print('return: {}'.format(s))


if __name__ == '__main__':

    main()
