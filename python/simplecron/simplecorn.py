import time
from datetime import datetime


class Scheduler(object):
    def __init__(self):
        self.jobs = []

    def run(self):
        [j.run() for j in self.jobs if j.is_established()]
       
    def add_job(self, job):
        self.jobs.append(job)


class Job(object):
    def __init__(self, condition_str, command):
        self.condition_str = condition_str
        self.create_conditions()
        self.command = command 

        self.last_execute_time = 0


    def create_conditions(self):
        fields = self.condition_str.split(' ')
        self.minute_str  = fields[0]
        self.hour_str    = fields[1]
        self.day_str     = fields[2]
        self.month_str   = fields[3]
        self.weekday_str = fields[4]

        if self.minute_str == '*':  self.minutes = [m for m in range(0, 60)]
        else:                       self.minutes = [int(s) for s in self.minute_str.split(',')]

        if self.hour_str == '*':    self.hours = [h for h in range(0, 24)]
        else:                       self.hours = [int(s) for s in self.hour_str.split(',')]

        if self.day_str == '*':     self.days = [d for d in range(1, 32)]
        else:                       self.days = [int(s) for s in self.day_str.split(',')]

        if self.month_str == '*':   self.months = [m for m in range(1, 13)]
        else:                       self.months = [int(s) for s in self.month_str.split(',')]

        if self.weekday_str == '*': self.weekdays = [d for d in range(0, 7)]
        else:                       self.weekdays = [int(s) for s in self.weekday_str.split(',')]


    def run(self):
        self.command.execute()
        self.last_execute_time = time.time()


    def __str__(self):
        return '{},{}'.format(self.condition_str, self.command)


    def get_datetime(self):
        return datetime.now()


    def is_established(self):
        if time.time() - self.last_execute_time < 60:
            return False

        now = self.get_datetime()
        
        if now.isoweekday() not in self.weekdays:
            return False
        
        if now.month not in self.months:
            return False

        if now.day not in self.days:
            return False

        if now.hour not in self.hours:
            return False

        if now.minute not in self.minutes:
            return False

        return True


class Action1Command(object):
    def execute(self):
        print('action1 at {}'.format(datetime.now()))


class Action2Command(object):
    def execute(self):
        print('action2 at {}'.format(datetime.now()))
        

if __name__ == '__main__':
    s = Scheduler()
    s.add_job(Job('* * * * *', Action1Command()))
    s.add_job(Job('10,11,12 * * * *', Action2Command()))

    while True:
        s.run()
        time.sleep(1)

