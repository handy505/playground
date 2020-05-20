#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import queue
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
    def __init__(self, inverters, outputpipeline):
        super().__init__()
        self.inverters = inverters
        self.outputpipeline = outputpipeline

    def run(self):
        while True:
            for inv in self.inverters:
                rec = inv.get_namedtuple_record()
                print('C: {}'.format(rec))
                self.outputpipeline.put(rec)

            time.sleep(1)


class RecorderThread(threading.Thread):
    def __init__(self, inputpipeline):
        super().__init__()
        self.inputpipeline = inputpipeline

    def run(self):
        while True:
            records = []
            while not self.inputpipeline.empty():
                rec = self.inputpipeline.get()
                records.append(rec)

            for rec in records:
                print('R: {}'.format(rec))

            time.sleep(3)


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.inverters = self.create_inverters()

        self.pipeline = queue.Queue()

        self.ct = CollectorThread(self.inverters, self.pipeline)
        self.rt = RecorderThread(self.pipeline)

    def run(self):
        self.ct.start()
        self.rt.start()

        while True:
            print('M: system maintain')
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
