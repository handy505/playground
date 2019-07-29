#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from inverter_base import InverterProxy
from collections import deque, namedtuple
from datetime import datetime
import time
from abc import ABCMeta, abstractmethod

MeterRecord = namedtuple( 'MeterRecord', ['ID', 'LoggedTime', 'Value'])



class MeterProxy(metaclass=ABCMeta):
    @abstractmethod
    def sync_with_hardware(self): pass

    @abstractmethod
    def create_record(self): pass


class TempMeterSimulator(MeterProxy):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return 'TMeter-{}'.format(self.id)

    def sync_with_hardware(self):
        self.Value = round(random.uniform(15,35))

    def create_record(self):
        dt = datetime.now().replace(microsecond=0)
        return MeterRecord(self.id, dt, self.Value)

class IlluMeterSimulator(MeterProxy):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return 'IMeter-{}'.format(self.id)

    def sync_with_hardware(self):
        self.Value = round(random.uniform(100,1000))

    def create_record(self):
        dt = datetime.now().replace(microsecond=0)
        return MeterRecord(self.id, dt, self.Value)

if __name__ == '__main__':
    meters = [IlluMeterSimulator(248), TempMeterSimulator(249)]
    print(meters)

    for m in meters:
        m.sync_with_hardware()
        rec = m.create_record()
        print(rec)
        time.sleep(3)



