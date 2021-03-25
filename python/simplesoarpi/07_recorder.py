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

    def get_string_record(self):
        result = '{},{},{},{}'.format(self.id, datetime.now(), self.kw, self.kwh)
        return result

    def get_record_object(self):
        return Record(self.id, self.kw, self.kwh)

    def get_namedtuple_record(self):
        return Record(self.id, datetime.now(), self.kw, self.kwh)

# -------------------------------------------------------------------------------------
class CollectorThread(threading.Thread):
    def __init__(self, inverters):
        super().__init__()
        self.inverters = inverters

    def run(self):
        while True:
            for inv in self.inverters:
                rec = inv.get_namedtuple_record()
                print('collectorthread: {}'.format(rec))
            time.sleep(1)


class RecorderThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            print('RecorderThread: ')
            time.sleep(1)


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.inverters = self.create_inverters()

        self.ct = CollectorThread(self.inverters)
        self.rt = RecorderThread()

    def run(self):
        self.ct.start()
        self.rt.start()

        while True:
            print('mainthread: system maintain')
            time.sleep(3)

    def create_inverters(self):
        result = [] 
        for id in range(1, 3):
            inv = Inverter(id)
            result.append(inv)
        return result


def main():
    mainthread = MainThread()
    mainthread.start()


if __name__ == '__main__':
    main()
