import time
import datetime
from collections import namedtuple

'''    
High Level
    Inverters
    Records

Low Level
    Scheduler
    Collector, BusHandler
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
class Device(object):
    def sync_with_hardware(self): pass
    def read_memorymapping(self): pass

class DCBoxMeter(Device): pass
class ADTecMeter(Device): pass
class SimuMeter(Device): pass
class SimuInverter(Device): pass

AlarmEvent = namedtuple('AlarmEvent', 'id logtime beforecode aftercode')
ErrorEvent = namedtuple('ErrorEvent', 'id logtime beforecode aftercode')

class AblerexInverter(Device):
    def __init__(self, id):
        self.id = id
    def __repr__(self):
        return 'AInv-{}'.format(self.id)
    def sync_with_hardware(self):
        print('AInv-{}.sync_with_hardware()'.format(self.id))
    def get_alarm_event(self):
        return AlarmEvent(self.id, datetime.datetime.now(), 0x00, 0x01)

class KACOInverter(Device):
    def __init__(self, id):
        self.id = id
    def __repr__(self):
        return 'KInv-{}'.format(self.id)
    def sync_with_hardware(self):
        print('KInv-{}.sync_with_hardware()'.format(self.id))


# ----------------------------------------------------




def inverters_factory():
    ablerex_inverters = [AblerexInverter(i) for i in range(1,5)]
    kaco_inverters = [KACOInverter(i) for i in range(5,8)]
    result = ablerex_inverters + kaco_inverters
    return result
        

    

def main():

    '''configurations = 'string'
    inverters = inverters_factory(configurations)
    meters = meter_factory(configurations)

    if is_concat_mode(configurations):
        concat_thread = ConcatThread()

    collector_thread = CollectorThread()
    recorder_thread = RecorderThread()
    uploader_thread = UploaderThread()
    '''

    
    inverters = inverters_factory()
    [print(inv) for inv in inverters]



    ae = AlarmEvent(1, datetime.datetime.now(), 0x00, 0x01)
    ee = ErrorEvent(1, datetime.datetime.now(), 0x00, 0x01)
    print(ae.beforecode)
    print(ee)


    while True:
        for inv in inverters:
            inv.sync_with_hardware()
            time.sleep(1)


if __name__ == '__main__':
    main()
