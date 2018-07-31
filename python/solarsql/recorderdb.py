#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
import random
import queue
import sys


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
            UID         INTEGER PRIMARY KEY AUTOINCREMENT,
            MID         INTEGER NOT NULL,
            DATETIME    TEXT NOT NULL,
            KW          REAL NOT NULL,
            KWH         REAL NOT NULL,
            UPLOADED    INTERGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)

        sql = ''' 
        CREATE TABLE IF NOT EXISTS measurehour (
            UID         INTEGER PRIMARY KEY AUTOINCREMENT,
            MID         INTEGER NOT NULL,
            DATETIME    TEXT NOT NULL,
            KW          REAL NOT NULL,
            KWH         REAL NOT NULL,
            UPLOADED    INTERGER NOT NULL DEFAULT 0
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





def main():
    pass

if __name__ == '__main__':
    main()
