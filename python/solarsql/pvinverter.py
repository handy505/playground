#!/usr/bin/env python3
import time
import random

import event


class Measurement(object):
    def __init__(self, mid, timestamp):
        self.mid = mid
        self.timestamp = timestamp
        self.OutputPower = 0
        self.ACVolPhaseA = 0
        self.ACVolPhaseB = 0
        self.ACVolPhaseC = 0
        self.ACFrequency = 0
        self.ACOutputCurrentA = 0
        self.ACOutputCurrentB = 0
        self.ACOutputCurrentC = 0
        self.DC1InputVol = 0
        self.DC2InputVol = 0
        self.DC1InputCurrent = 0
        self.DC2InputCurrent = 0
        self.DCBusPositiveVol = 0
        self.DCBusNegativeVol = 0
        self.InternalTemper = 0
        self.HeatSinkTemper = 0
        self.InputPowerA = 0
        self.InputPowerB = 0
        self.TotalOutputPower = 0

    def __str__(self):
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp))
        return '{}, {}, ..., {} kwh'.format(self.mid, ts, round(self.TotalOutputPower,3))


class PVInverter(object):
    def __init__(self, mid):
        self.mid = mid
        self.alarm_code = 0
        self.error_code = 0
        self.events = []


        # for simulate event interval
        self.event_timestamp = time.time()
       
        # measurement 
        self.OutputPower = 0
        self.ACVolPhaseA = 0
        self.ACVolPhaseB = 0
        self.ACVolPhaseC = 0
        self.ACFrequency = 0
        self.ACOutputCurrentA = 0
        self.ACOutputCurrentB = 0
        self.ACOutputCurrentC = 0
        self.DC1InputVol = 0
        self.DC2InputVol = 0
        self.DC1InputCurrent = 0
        self.DC2InputCurrent = 0
        self.DCBusPositiveVol = 0
        self.DCBusNegativeVol = 0
        self.InternalTemper = 0
        self.HeatSinkTemper = 0
        self.InputPowerA = 0
        self.InputPowerB = 0
        self.TotalOutputPower = 0


    def __str__(self):
        return 'Inverter-{}, {} kwh, {} events'.format(self.mid, round(self.TotalOutputPower,3), len(self.events))


    def sync_with_hardware(self):
        time.sleep(random.randint(50,200)/1000)

        # alarm event
        if time.time() - self.event_timestamp > (60*3):
            current_code = random.randint(0,16)
            if current_code != self.alarm_code:
                origin_event = event.AlarmEvent(self.mid, time.time(), self.alarm_code, current_code)
                [self.events.append(ablerex_alarm_event) for ablerex_alarm_event in origin_event.to_ablerex_format_records()]
                self.alarm_code = current_code
            self.event_timestamp = time.time()
                

        # measurement
        self.OutputPower = random.randint(0,1000) * 0.01
        self.ACVolPhaseA = random.randint(0,1000)
        self.ACVolPhaseB = random.randint(0,1000)
        self.ACVolPhaseC = random.randint(0,1000)
        self.ACFrequency = 600 * 0.1
        self.ACOutputCurrentA = random.randint(0,1000) * 0.1
        self.ACOutputCurrentB = random.randint(0,1000) * 0.1
        self.ACOutputCurrentC = random.randint(0,1000) * 0.1
        self.DC1InputVol = random.randint(0,1000)
        self.DC2InputVol = random.randint(0,1000)
        self.DC1InputCurrent = random.randint(0,1000) * 0.1
        self.DC2InputCurrent = random.randint(0,1000) * 0.1 
        self.DCBusPositiveVol = random.randint(0,1000)
        self.DCBusNegativeVol = random.randint(0,1000)
        self.InternalTemper = random.randint(0,1000)
        self.HeatSinkTemper = random.randint(0,1000)
        self.InputPowerA = random.randint(0,1000) * 0.01
        self.InputPowerB = random.randint(0,1000) * 0.01
        self.TotalOutputPower += random.randint(0,10)


    def make_record(self):
        result = Measurement(self.mid, time.time())
        result.OutputPower = round(self.OutputPower, 2)
        result.ACVolPhaseA = self.ACVolPhaseA 
        result.ACVolPhaseB = self.ACVolPhaseB 
        result.ACVolPhaseC = self.ACVolPhaseC 
        result.ACFrequency = round(self.ACFrequency, 1)
        result.ACOutputCurrentA = round(self.ACOutputCurrentA, 1)
        result.ACOutputCurrentB = round(self.ACOutputCurrentB, 1)
        result.ACOutputCurrentC = round(self.ACOutputCurrentC, 1)
        result.DC1InputVol = round(self.DC1InputVol, 1)
        result.DC2InputVol = round(self.DC2InputVol, 1)
        result.DC1InputCurrent = round(self.DC1InputCurrent, 1)
        result.DC2InputCurrent = round(self.DC2InputCurrent, 1)
        result.DCBusPositiveVol = self.DCBusPositiveVol 
        result.DCBusNegativeVol = self.DCBusNegativeVol 
        result.InternalTemper = self.InternalTemper 
        result.HeatSinkTemper = self.HeatSinkTemper 
        result.InputPowerA = round(self.InputPowerA, 2)
        result.InputPowerB = round(self.InputPowerB, 2)
        result.TotalOutputPower = self.TotalOutputPower 
        return result


