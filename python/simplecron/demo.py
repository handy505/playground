import time
from datetime import datetime
from simplecron import Scheduler, Job


class Action1Command(object):
    def execute(self):
        print('action1 at {}'.format(datetime.now()))


class Action2Command(object):
    def execute(self):
        print('action2 at {}'.format(datetime.now()))
        

if __name__ == '__main__':
    s = Scheduler()
    s.add_job(Job('* * * * *', Action1Command()))
    s.add_job(Job('8,10,11,12 * * * *', Action2Command()))

    while True:
        s.run()

'''
$ python3 demo.py 
action1 at 2020-12-23 16:06:28.065473
action1 at 2020-12-23 16:07:28.065611
action2 at 2020-12-23 16:08:00.000023
action1 at 2020-12-23 16:08:28.065712
action1 at 2020-12-23 16:09:28.065797
action2 at 2020-12-23 16:10:00.000005
action1 at 2020-12-23 16:10:28.065891
action2 at 2020-12-23 16:11:00.000119
action1 at 2020-12-23 16:11:28.065993
action2 at 2020-12-23 16:12:00.000221
action1 at 2020-12-23 16:12:28.066152
action1 at 2020-12-23 16:13:28.066242

'''
