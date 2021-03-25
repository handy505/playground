import time
import threading
from datetime import datetime


from cronscheduler import Scheduler, Job
from dbhandler import DBHandler
from machine import Machine
import commands as cmd



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

    machines = [Machine(id) for id in range(1,4)]
    commands = [cmd.SyncWithHardwareCommand(m) for m in machines]


    csch = Scheduler()
    [csch.add_job(Job('* * * * *', c)) for c in commands]


    dbhandler = DBHandler()
    c = cmd.InsertAllMachineRecordToDatabaseCommand(machines, dbhandler)
    csch.add_job(Job('* * * * *', c))


    usch = Scheduler()
    usch.add_job(Job('*/3 * * * *', cmd.UploadUnuploadedRecordsCommand(dbhandler)))


    cthread = CollectorThread(csch)
    uthread = UploaderThread(usch)

    cthread.start()
    uthread.start()

    cthread.join()
    uthread.join()


