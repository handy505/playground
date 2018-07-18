#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
import random
import queue

class Record(object):
    def __init__(self, mid, timestamp, v1, v2):
        self.mid = mid
        self.timestamp = timestamp
        self.v1 = v1
        self.v2 = v2
    def __str__(self):
        ts=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.timestamp))
        return '{},{},{},{}'.format(self.mid, ts, self.v1, self.v2)


class Collector(threading.Thread):
    def __init__(self, oqueue):
        threading.Thread.__init__(self)       
        self.oqueue = oqueue

    def run(self):
        while True:
            v1 = random.randint(100, 200)
            v2 = random.randint(1000, 5000)
            r = Record(1, time.time(), v1, v2)
            print('C: {}'.format(r))
            self.oqueue.put(r)
            time.sleep(1)





class RecorderDB(threading.Thread):
    def __init__(self, iqueue, oqueue, fbqueue):
        threading.Thread.__init__(self)       
        self.oqueue = oqueue
        self.iqueue = iqueue
        self.oqueue = oqueue
        self.fbqueue = fbqueue


    def run(self):
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

        while True:
            while not self.iqueue.empty():
                rec = self.iqueue.get()
                print('R: {}, iqueue size: {}'.format(rec, self.iqueue.qsize()))

                c = self.dbconn.cursor()
                c.execute( "INSERT INTO measure VALUES (NULL, ?, datetime('now', 'localtime'), ?, ?, 0)",
                    (rec.mid, rec.v1, rec.v2))
                self.dbconn.commit()


            time.sleep(2)

    def run_old(self):
        #conn = sqlite3.connect('data.db')
        #while True:
        if self.dbconn:
            ts = time.time()
            watt = random.randint(100, 200)
            kwh = random.randint(1000, 5000)
            print('collector {}, {}, {}'.format(time.time(), watt, kwh))

            c = conn.cursor()
            c.execute( "INSERT INTO measure VALUES (NULL, datetime('now', 'localtime'), ?, ?)",
                (watt, kwh))
            conn.commit()

            time.sleep(1)


class Uploader(threading.Thread):
    def __init__(self, iqueue, oqueue):
        threading.Thread.__init__(self)       
        self.iqueue = iqueue
        self.oqueue = oqueue

    def run(self):
        while True:
            print('U: {}'.format(time.time()))
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
