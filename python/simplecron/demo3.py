import time
import threading
from datetime import datetime
from collections import namedtuple


from simplecron import Scheduler, Job
from dbhandler import DBHandler

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


class UploadUnuploadedRecords(object):
    def __init__(self, dbhandler):
        self.dbhandler = dbhandler

    def execute(self):
        rows = self.dbhandler.read_unuploaded_rows()
        [print(r) for r in rows]
        time.sleep(10)
        print('(DEBUG) UploadUnuploadedRecords.execute() at {}'.format(datetime.now()))

        uids = [r[0] for r in rows]
        [self.dbhandler.update_uploaded_row_by_uid(uid) for uid in uids]


# Keep SRP !!!
class CollectorThread(threading.Thread):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    def run(self):
        while True:
            self.scheduler.run()
            

class UploaderThread(threading.Thread):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    def run(self):
        while True:
            self.scheduler.run()


if __name__ == '__main__':

    csch = Scheduler()

    machines = [Machine(id) for id in range(1,4)]

    commands = [SyncWithHardwareCommand(m) for m in machines]
    [csch.add_job(Job('* * * * *', c)) for c in commands]

    dbhandler = DBHandler()
    c = InsertAllMachineRecordToDatabaseCommand(machines, dbhandler)
    csch.add_job(Job('* * * * *', c))



    usch = Scheduler()
    usch.add_job(Job('*/3 * * * *', UploadUnuploadedRecords(dbhandler)))



    cthread = CollectorThread(csch)
    uthread = UploaderThread(usch)

    cthread.start()
    uthread.start()

    cthread.join()
    uthread.join()


