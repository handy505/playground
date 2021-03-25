import time
from datetime import datetime
from collections import namedtuple


from simplecron import Scheduler, Job
from dbproxy import DBHandler

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


class SyncWithHardwareCommand(object):
    def __init__(self, machine):
        self.machine = machine

    def execute(self):
        self.machine.sync_with_hardware()


class InsertAllMachineRecordToDatabaseCommand(object):
    def __init__(self, machines, dbhandler):
        self.machines = machines
        self.dbhandler = dbhandler
   
    def execute(self):
        for m in self.machines:
            r = m.get_record()
            self.dbhandler.insert_record(r)

        print('(DEBUG) InsertAllMachineRecordToDatabaseCommand.execute() at {}'.format(datetime.now()))



if __name__ == '__main__':

    s = Scheduler()

    machines = [Machine(id) for id in range(1,4)]

    commands = [SyncWithHardwareCommand(m) for m in machines]
    [s.add_job(Job('* * * * *', c)) for c in commands]

    dbhandler = DBHandler()
    c = InsertAllMachineRecordToDatabaseCommand(machines, dbhandler)
    s.add_job(Job('* * * * *', c))


    while True:
        s.run()

