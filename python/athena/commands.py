import time
from datetime import datetime


from cronscheduler import Scheduler, Job
from dbhandler import DBHandler
from machine import Machine


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


class UploadUnuploadedRecordsCommand(object):
    def __init__(self, dbhandler):
        self.dbhandler = dbhandler

    def execute(self):
        rows = self.dbhandler.read_unuploaded_rows()
        [print(r) for r in rows]
        time.sleep(10)
        print('(DEBUG) UploadUnuploadedRecordsCommand.execute() at {}'.format(datetime.now()))

        uids = [r[0] for r in rows]
        [self.dbhandler.update_uploaded_row_by_uid(uid) for uid in uids]

