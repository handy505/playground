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

        self.inverters = []
        for id in range(1, 3):
            inv = devices.Inverter(id)
            print(inv)
            self.inverters.append(inv)

        #self.imeter = devices.DCBoxIlluMeter(11)
        #self.tmeter = devices.DCBoxTempMeter(10)

        self.modbuslistener = concatenate.ModbusListener(self.inverters, 
                                                         self.imeter, 
                                                         self.tmeter)

    def run(self):
        refresh_timestamp = time.time()
        self.modbuslistener.start()
        while True:
            now = time.time()
            if now - refresh_timestamp > 3:

                #[inv.refresh() for inv in self.inverters]
                #self.imeter.refresh()
                #self.tmeter.refresh()

                refresh_timestamp = now


def main():
    print('PV Inverter simulator')
    mainthread = MainThread()
    mainthread.start()


if __name__ == '__main__':

    main()
