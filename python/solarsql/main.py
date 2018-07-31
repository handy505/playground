#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
import random
import queue
import sys

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
        return 'Inverter-{}, {:>7.3f} kw, {:>7.3f} kwh'.format(self.mid, round(self.kw,3), round(self.kwh,3))

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



class RecorderDB(threading.Thread):
    def __init__(self, iqueue, oqueue, fbqueue):
        threading.Thread.__init__(self)       
        self.oqueue = oqueue
        self.iqueue = iqueue
        self.oqueue = oqueue
        self.fbqueue = fbqueue

        self.commit_timestamp = time.time()

    def run(self):
        '''
        tables:
            event
            measure
            measure_hourly
            illu
            illu_hourly
            temp
            temp_hourly
        '''
        self.dbconn = sqlite3.connect('data.db')
        c = self.dbconn.cursor()
        sql = ''' 
        CREATE TABLE IF NOT EXISTS measure (
            UID INTEGER PRIMARY KEY AUTOINCREMENT,
            MID INTEGER NOT NULL,
            DATETIME TEXT NOT NULL,
            WATT REAL NOT NULL,
            KWH REAL NOT NULL,
            UPLOADED INTERGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)

        minutely_localtime = time.localtime()
        hourly_localtime = time.localtime()

        while True:


            if time.localtime().tm_min != minutely_localtime.tm_min:
                # every minute
                self.minutely_operation()
                minutely_localtime = time.localtime()


            if time.localtime().tm_hour != hourly_localtime.tm_hour:
                # every hour
                self.hourly_operation()
                hourly_localtime = time.localtime()


            time.sleep(3)


    def minutely_operation(self):
        recs = []
        while not self.iqueue.empty():
            rec = self.iqueue.get()
            recs.append(rec)




        start  = time.time()
        for rec in recs:
            c = self.dbconn.cursor()
            '''c.execute( "INSERT INTO measure VALUES (NULL, ?, datetime('now', 'localtime'), ?, ?, 0)", 
                (rec.mid, rec.v1, rec.v2))
                '''
            c.execute( "INSERT INTO measure VALUES (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, 0)", 
                (rec.mid, rec.timestamp, rec.kw, rec.kwh))
        print('Insert database: {} seconds'.format(round((time.time()-start),6)))

        if time.time() - self.commit_timestamp > (60*10):
            start = time.time()
            self.dbconn.commit()
            print('Commit database: {} seconds'.format(round((time.time()-start),6)))
            self.commit_timestamp = time.time()


    def hourly_operation(self):
        print('hour_operation()')
        pass



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
    rt = RecorderDB(aqueue, bqueue, cqueue)
    ut = Uploader(bqueue, cqueue)

    ct.start()
    rt.start()
    ut.start()

    ct.join()
    rt.join()
    ut.join()



if __name__ == '__main__':
    main()
