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
        return '{}, {}, {} kw, ..., {} kwh'.format(self.mid, ts, self.OutputPower, self.TotalOutputPower)


class PVInverter(object):
    def __init__(self, mid):
        self.mid = mid
        self.alarm_code = 0
        self.error_code = 0
        self.events = []


        # for simulate event interval
        self.event_timestamp = time.time()
        self.kw = 0
        self.kwh = 1000
       
        # real
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
        return 'Inverter-{}, {:>5.3f} kw, {:>7.3f} kwh, {} events'.format(
            self.mid, round(self.OutputPower,3), round(self.TotalOutputPower,3), len(self.events))

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
        self.kw = (random.randint(0,1000)/1000)
        self.kwh += self.kw


        self.OutputPower = random.randint(0,1000)
        self.ACVolPhaseA = random.randint(0,1000)
        self.ACVolPhaseB = random.randint(0,1000)
        self.ACVolPhaseC = random.randint(0,1000)
        self.ACFrequency = random.randint(0,1000)
        self.ACOutputCurrentA = random.randint(0,1000)
        self.ACOutputCurrentB = random.randint(0,1000)
        self.ACOutputCurrentC = random.randint(0,1000)
        self.DC1InputVol = random.randint(0,1000)
        self.DC2InputVol = random.randint(0,1000)
        self.DC1InputCurrent = random.randint(0,1000)
        self.DC2InputCurrent = random.randint(0,1000)
        self.DCBusPositiveVol = random.randint(0,1000)
        self.DCBusNegativeVol = random.randint(0,1000)
        self.InternalTemper = random.randint(0,1000)
        self.HeatSinkTemper = random.randint(0,1000)
        self.InputPowerA = random.randint(0,1000)
        self.InputPowerB = random.randint(0,1000)
        self.TotalOutputPower = random.randint(0,1000)


    def make_record(self):
        result = Measurement(self.mid, time.time())
        result.OutputPower = self.OutputPower 
        result.ACVolPhaseA = self.ACVolPhaseA 
        result.ACVolPhaseB = self.ACVolPhaseB 
        result.ACVolPhaseC = self.ACVolPhaseC 
        result.ACFrequency = self.ACFrequency 
        result.ACOutputCurrentA = self.ACOutputCurrentA 
        result.ACOutputCurrentB = self.ACOutputCurrentB 
        result.ACOutputCurrentC = self.ACOutputCurrentC 
        result.DC1InputVol = self.DC1InputVol 
        result.DC2InputVol = self.DC2InputVol 
        result.DC1InputCurrent = self.DC1InputCurrent 
        result.DC2InputCurrent = self.DC2InputCurrent 
        result.DCBusPositiveVol = self.DCBusPositiveVol 
        result.DCBusNegativeVol = self.DCBusNegativeVol 
        result.InternalTemper = self.InternalTemper 
        result.HeatSinkTemper = self.HeatSinkTemper 
        result.InputPowerA = self.InputPowerA 
        result.InputPowerB = self.InputPowerB 
        result.TotalOutputPower = self.TotalOutputPower 
        return result


