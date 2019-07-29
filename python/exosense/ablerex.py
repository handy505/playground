#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from inverter_base import InverterProxy
from collections import deque, namedtuple
from datetime import datetime
import time

InverterRecord = namedtuple(
    'InverterRecord', 
    [ 'ID',
      'LoggedTime',
      'DC1Voltage', 'DC2Voltage', 'DC3Voltage', 'DC4Voltage', 
      'DC1Current', 'DC2Current', 'DC3Current', 'DC4Current',
      'DC1Power', 'DC2Power', 'DC3Power', 'DC4Power',
      'DCPositive', 'DCNegative', 
      'InternalTemp', 'HeatSinkTemp', 
      'AC1Voltage', 'AC2Voltage', 'AC3Voltage',
      'AC1Current', 'AC2Current', 'AC3Current',
      'ACFrequency', 'ACOutputPower', 
      'KWH',
    ])


def create_ablerex_inverter_simulators(since, to):
    result = []
    for i in range(since, to+1):
        inv = AblerexInverterSimulator(i, serport=None)
        result.append(inv)
    return result


class AblerexInverterSimulator(InverterProxy):
    def __init__(self, id):
        self.id = id
        self.KWH = 0

    def __repr__(self):
        return 'Inverter-{}'.format(self.id)

    def sync_with_hardware(self):
        self.DC1Voltage = round(random.uniform(5,50))
        self.DC2Voltage = round(random.uniform(10,100))
        self.DC3Voltage = round(random.uniform(10,100))
        self.DC4Voltage = round(random.uniform(10,100))

        self.DC1Current = round(random.uniform(10,100))
        self.DC2Current = round(random.uniform(10,100))
        self.DC3Current = round(random.uniform(10,100))
        self.DC4Current = round(random.uniform(10,100))

        self.DC1Power = round(random.uniform(10,100))
        self.DC2Power = round(random.uniform(10,100))
        self.DC3Power = round(random.uniform(10,100))
        self.DC4Power = round(random.uniform(10,100))

        self.DCPositive = round(random.uniform(10,100))
        self.DCNegative = round(random.uniform(10,100))

        self.InternalTemp = round(random.uniform(10,100))
        self.HeatSinkTemp = round(random.uniform(10,100))

        self.AC1Voltage = round(random.uniform(10,100))
        self.AC2Voltage = round(random.uniform(10,100))
        self.AC3Voltage = round(random.uniform(10,100))

        self.AC1Current = round(random.uniform(10,100))
        self.AC2Current = round(random.uniform(10,100))
        self.AC3Current = round(random.uniform(10,100))

        self.ACFrequency = round(random.uniform(10,100))
        self.ACOutputPower = round(random.uniform(10,100))
        
        self.KWH = self.KWH + round(random.uniform(10,20))
 
    def create_record(self):
        return InverterRecord( self.id,
                               datetime.now().replace(microsecond=0),
                               self.DC1Voltage, self.DC2Voltage, self.DC3Voltage, self.DC4Voltage,
                               self.DC1Current, self.DC2Current, self.DC3Current, self.DC4Current,
                               self.DC1Power, self.DC2Power, self.DC3Power, self.DC4Power,
                               self.DCPositive, self.DCNegative,
                               self.InternalTemp, self.HeatSinkTemp,
                               self.AC1Voltage, self.AC2Voltage, self.AC3Voltage,
                               self.AC1Current, self.AC2Current, self.AC3Current,
                               self.ACFrequency, self.ACOutputPower,
                               self.KWH
                             )


if __name__ == '__main__':
    inverters = [AblerexInverterSimulator(id) for id in range(1,7+1)]
    print(inverters)

    for inv in inverters:
        inv.sync_with_hardware()
        rec = inv.create_record()
        print(rec)
        time.sleep(3)



