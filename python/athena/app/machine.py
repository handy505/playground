import time
from datetime import datetime
from collections import namedtuple

Record = namedtuple('Record', ['DeviceID', 'LoggedDatetime', 'KW', 'KWH'])


class Machine(object):
    def __init__(self, id):
        self.id = id
        self.kw = 52
        self.kwh = 100

    def __str__(self):
        return 'Machine-{}'.format(self.id)

    def sync_with_hardware(self):
        time.sleep(0.2)
        print('(DEBUG) {} sync_with_hardware at {}'.format(self, datetime.now()))

    def get_record(self):
        return Record(self.id, datetime.now(), self.kw, self.kwh)
