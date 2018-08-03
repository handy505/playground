#!/usr/bin/env python3
import time
import random

import event

class InverterMeasurement(object):
    def __init__(self, mid, timestamp, kw, kwh):
        self.mid = mid
        self.timestamp = timestamp
        self.kw = kw 
        self.kwh = kwh

    def __str__(self):
        ts = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.timestamp))
        return '{},{},{},{}'.format(self.mid, ts, self.kw, self.kwh)



class PVInverter(object):
    def __init__(self, mid):
        self.mid = mid
        self.alarm_code = 0
        self.error_code = 0
        self.events = []
        self.kw = 0
        self.kwh = 1000
       
    def __str__(self):
        return 'Inverter-{}, {:>5.3f} kw, {:>7.3f} kwh, {} events'.format(
            self.mid, round(self.kw,3), round(self.kwh,3), len(self.events))

    def sync_with_hardware(self):
        time.sleep(random.randint(50,200)/1000)

        # alarm event
        current_code = random.randint(0,16)
        if current_code != self.alarm_code:
            oe = event.AlarmEvent(self.mid, time.time(), self.alarm_code, current_code)
            [self.events.append(aae) for aae in oe.to_ablerex_format_records()]
            self.alarm_code = current_code
                
        # measurement
        self.kw = (random.randint(0,1000)/1000)
        self.kwh += self.kw

    def make_record(self):
        return InverterMeasurement(self.mid, time.time(), round(self.kw,3), round(self.kwh,0))

