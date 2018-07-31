#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
import random
import queue
import sys

import recorderdb

class InverterRecord(object):
    def __init__(self, mid, timestamp, kw, kwh):
        self.mid = mid
        self.timestamp = timestamp
        self.kw = kw 
        self.kwh = kwh

    def __str__(self):
        ts = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.timestamp))
        return '{},{},{},{}'.format(self.mid, ts, self.kw, self.kwh)


class PVInverter(object):
    def __init__(self, mid):
        self.mid = mid
        self.alarm_code = 0
        self.error_code = 0
        self.kw = 0
        self.kwh = 0
       
    def __str__(self):
        return 'Inverter-{}, {:>5.3f} kw, {:>7.3f} kwh'.format(self.mid, round(self.kw,3), round(self.kwh,3))

    def sync_with_hardware(self):
        time.sleep(random.randint(50,200)/1000)
        self.kw = (random.randint(0,1000)/1000)
        self.kwh += self.kw

    def make_record(self):
        return InverterRecord(self.mid, time.time(), round(self.kw,3), round(self.kwh,3))



class Collector(threading.Thread):
    def __init__(self, oqueue):
        threading.Thread.__init__(self)       
        self.oqueue = oqueue


    def run(self):
    
        pvgroup = [PVInverter(i) for i in range(1,3)]
        [print(pv) for pv in pvgroup]


        ltime = time.localtime()
        while True:

            for pv in pvgroup:
                pv.sync_with_hardware()
                print(pv)


            if time.localtime().tm_min != ltime.tm_min:
                ltime = time.localtime()
                print('New minute: {}'.format(ltime.tm_min))

                for pv in pvgroup:
                    r = pv.make_record()
                    print('Get new records: {}'.format(r))
                    self.oqueue.put(r)


            time.sleep(1)



class Uploader(threading.Thread):
    def __init__(self, iqueue, oqueue):
        threading.Thread.__init__(self)       
        self.iqueue = iqueue
        self.oqueue = oqueue

    def run(self):
        while True:
            #print('U: {}'.format(time.time()))
            time.sleep(1)


def main():

    aqueue = queue.Queue()
    bqueue = queue.Queue()
    cqueue = queue.Queue()

    ct = Collector(aqueue)
    rt = recorderdb.RecorderDB(aqueue, bqueue, cqueue)
    ut = Uploader(bqueue, cqueue)

    ct.start()
    rt.start()
    ut.start()

    ct.join()
    rt.join()
    ut.join()


if __name__ == '__main__':
    main()
