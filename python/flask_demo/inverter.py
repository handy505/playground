#!/usr/bin/env python3
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
        return self.get_namedtuple_record()

    def get_namedtuple_record(self):
        return Record(self.id, datetime.now(), self.kw, self.kwh)
