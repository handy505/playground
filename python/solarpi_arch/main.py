import time
import datetime
import random
from collections import namedtuple
from collections import deque 

'''    
High Level
    Inverters
    Records

Low Level
    Scheduler, Collector, BusHandler, Service
    GUI
    Hearbeat
    Concat 
    Uploader
'''


# ----------------------------------------------------
# High Level
# ----------------------------------------------------
class Record():
    def format_to_ablerex(self): pass

class EventRecord(Record): pass

class MeasurementRecord(Record): pass

# ----------------------------------------------------
# High Level
# ----------------------------------------------------
AlarmEvent = namedtuple('AlarmEvent', 'id logtime beforecode aftercode')
ErrorEvent = namedtuple('ErrorEvent', 'id logtime beforecode aftercode')

class Device(object):
    def sync_with_hardware(self): pass
    def read_memorymapping(self): pass


class AblerexInverter(Device):
    def __init__(self, id):
        self.id = id
        self.alarm_code = 0x00
        self.error_code = 0x00
        self.volt = 0
        self.current = 0

    def __repr__(self):
        return 'Ablerex-{}'.format(self.id)

    def sync_with_hardware(self):
        print('Ablerex-{}.sync_with_hardware()'.format(self.id))

    def get_alarm_event(self):
        return AlarmEvent(self.id, datetime.datetime.now(), 0x00, 0x01)


class KACOInverter(Device):
    def __init__(self, id):
        self.id = id
        self.volt = 0
        self.current = 0

    def __repr__(self):
        return 'KACO-{}'.format(self.id)

    def sync_with_hardware(self):
        print('KACO-{}.sync_with_hardware()'.format(self.id))


class SimuInverter(Device):
    def __init__(self, id):
        self.id = id
        self.alarm_codes = deque()
        self.error_codes = deque()
        self.alarm_events = []
        self.error_events = []
        self.volt = 0
        self.current = 0

    def __repr__(self):
        return 'Simu-{}'.format(self.id)

    def sync_with_hardware(self):
        print('Simu-{}.sync_with_hardware()'.format(self.id))
        self.alarm_codes.append(random.randint(0,1))
        self.error_codes.append(random.randint(0,1))
        self.volt       = random.randint(100,200)
        self.current    = random.randint(10,100)


class DCBoxMeter(Device): pass

class ADTecMeter(Device): pass

class SimuMeter(Device): pass

def inverters_factory():
    result = [
        AblerexInverter(1),
        KACOInverter(2),
        SimuInverter(3),
    ]
    return result

# ----------------------------------------------------
def main():

    inverters = inverters_factory()
    [print(inv) for inv in inverters]

    for inv in inverters:
        inv.sync_with_hardware()
        time.sleep(1)


if __name__ == '__main__':
    main()


'''
pi@raspberrypi:~/demo/python/solarpi_arch $ python3 main.py 
Ablerex-1
KACO-2
Simu-3
Ablerex-1.sync_with_hardware()
KACO-2.sync_with_hardware()
Simu-3.sync_with_hardware()
'''
