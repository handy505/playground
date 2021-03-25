#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
import threading
from datetime import datetime
from collections import namedtuple


Record = namedtuple('Record', ['DeviceID', 'LoggedDatetime', 'KW', 'KWH'])


class Inverter(object):
    def __init__(self, id):
        self.id = id
        self.kw = 52
        self.kwh = 100
    
    def __str__(self):
        return 'Inverter-{}'.format(self.id)

    def get_record(self):
        return Record(self.id, datetime.now(), self.kw, self.kwh)


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.inverters = []
        for id in range(1, 3):
            inv = Inverter(id)
            self.inverters.append(inv)


    def run(self):
        while True:
            for inv in self.inverters:
                rec = inv.get_record()
                print(rec)
            print('---')
            time.sleep(1)


def main():
    mainthread = MainThread()
    mainthread.start()

if __name__ == '__main__':
    main()
