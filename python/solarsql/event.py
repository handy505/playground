#!/usr/bin/env python3
import time
import sys


class Event(object):
    def __init__(self, mid, timestamp, older_code, newer_code):
        self.mid = mid
        self.timestamp = timestamp
        self.older_code = older_code 
        self.newer_code = newer_code 


class AlarmEvent(Event):
    def __init__(self, mid, timestamp, older_code, newer_code):
        super().__init__(mid, timestamp, older_code, newer_code)

    def to_ablerex_format_records(self):
        results = []
        for shift in range(0, 8):
            mask = 0x01 << shift
            newerbit = self.newer_code & mask
            olderbit = self.older_code & mask
            if olderbit != newerbit:
                stat = 'H' if newerbit else 'R'
                ablerex_event = AblerexEvent(self.mid, self.timestamp, 1, shift, stat)
                results.append(ablerex_event)
        return results


class ErrorEvent(Event):
    def __init__(self, mid, timestamp, older_code, newer_code):
        super().__init__(mid, timestamp, older_code, newer_code)

    def to_ablerex_format_records(self):
        results = []
        for shift in range(0, 8):
            mask = 0x01 << shift
            newerbit = self.newer_code & mask
            olderbit = self.older_code & mask
            if olderbit != newerbit:
                stat = 'H' if newerbit else 'R'
                ablerex_event = AblerexEvent(self.mid, self.timestamp, 2, shift, stat)
                results.append(ablerex_event)
        return results


class LinkEvent(Event):
    def __init__(self, mid, timestamp, older_code, newer_code):
        super().__init__(mid, timestamp, older_code, newer_code)

    def to_ablerex_format_records(self):
        if self.newer_code:
            return [AblerexEvent(self.mid, self.timestamp, 0, 100, 'H')]
        else:
            return [AblerexEvent(self.mid, self.timestamp, 0, 101, 'H')]


class AblerexEvent(object):
    def __init__(self, mid, timestamp, kind, code, stat, onlinecount=None):
        self.mid = mid
        self.timestamp = timestamp
        self.kind = kind 
        self.code = code
        self.stat = stat
        self.onlinecount = onlinecount
    
    def __str__(self):
        timestring = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp))
        return '{},{},{},{},{},{}'.format(
            self.mid, timestring, self.kind, self.code, self.stat, self.onlinecount)


if __name__ == '__main__':

    ae = AblerexEvent(1, time.time(), 1, 0, 'H', 3)
    print(ae)
