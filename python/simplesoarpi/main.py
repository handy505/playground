#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
import threading
from datetime import datetime
from collections import namedtuple

Record = namedtuple('Record', ['DeviceID', 'LoggedDatetime', 'KW', 'KWH'])

class RecordObj(object):
    def __init__(self, id, kw, kwh):
        self.id = id
        self.LoggedDatetime = datetime.now()
        self.kw = kw
        self.kwh = kwh

    def __str__(self):
        return '{},{},{},{}'.format(self.id, self.LoggedDatetime, self.kw, self.kwh)


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
                rec = inv.get_namedtuple_record()
                print(rec)
            print('---')
            time.sleep(1)


def main():
    mainthread = MainThread()
    mainthread.start()

if __name__ == '__main__':
    main()
