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


    def run(self):
        self.command.execute()
        self.last_execute_time = time.time()


    def __str__(self):
        return '{},{}'.format(self.condition_str, self.command)


    def create_conditions(self):
        fields = self.condition_str.split(' ')
        self.minute_str  = fields[0]
        self.hour_str    = fields[1]
        self.day_str     = fields[2]
        self.month_str   = fields[3]
        self.weekday_str = fields[4]

        self.minute_conditions  = self.create_minute_conditions(self.minute_str)
        self.hour_conditions    = self.create_hour_conditions(self.hour_str)
        self.day_conditions     = self.create_day_conditions(self.day_str)
        self.month_conditions   = self.create_month_conditions(self.month_str)
        self.weekday_conditions = self.create_weekday_conditions(self.weekday_str)


    def create_minute_conditions(self, minute_str):
        if minute_str == '*':   result = [m for m in range(0, 60)]
        elif '/' in minute_str: result = self._get_divided_conditions(minute_str, 0, 60)
        else:                   result = [int(s) for s in minute_str.split(',')]
        return result


    def create_hour_conditions(self, hour_str):
        if hour_str == '*':   result = [h for h in range(0, 24)]
        elif '/' in hour_str: result = self._get_divided_conditions(hour_str, 0, 24)
        else:                 result = [int(s) for s in hour_str.split(',')]
        return result


    def create_day_conditions(self, day_str):
        if self.day_str == '*': result = [d for d in range(1, 32)]
        elif '/' in day_str:    result = self._get_divided_conditions(day_str, 1, 32)
        else:                   result = [int(s) for s in day_str.split(',')]
        return result


    def create_month_conditions(self, month_str):
        if self.month_str == '*': result = [m for m in range(1, 13)]
        elif '/' in month_str:    result = self._get_divided_conditions(month_str, 1, 13)
        else:                     result = [int(s) for s in month_str.split(',')]
        return result


    def create_weekday_conditions(self, weekday_str):
        if weekday_str == '*':      result = [d for d in range(0, 7)]
        elif '/' in weekday_str:    result = self._get_divided_conditions(weekday_str, 0, 7)
        else:                       result = [int(s) for s in weekday_str.split(',')]
        return result


    def _get_divided_conditions(self, string, since, to):
        dividend, divisor = string.split('/')
        result = [h for h in range(since, to) if h % int(divisor) == 0]
        return result


    def get_datetime(self):
        return datetime.now()


    def is_enough_interval(self):
        return time.time() - self.last_execute_time > 60


    def is_established(self):
        if not self.is_enough_interval():
            return False

        now = self.get_datetime()
        
        if now.isoweekday() not in self.weekday_conditions:
            return False
        
        if now.month not in self.month_conditions:
            return False

        if now.day not in self.day_conditions:
            return False

        if now.hour not in self.hour_conditions:
            return False

        if now.minute not in self.minute_conditions:
            return False

        return True

