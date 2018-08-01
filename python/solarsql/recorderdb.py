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
        CREATE TABLE IF NOT EXISTS event(
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            older       INTEGER NOT NULL,
            newer       INTEGER NOT NULL,
            uploaded    INTERGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


        sql = ''' 
        CREATE TABLE IF NOT EXISTS measure (
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            kw          REAL NOT NULL,
            kwh         REAL NOT NULL,
            uploaded    INTERGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


        sql = ''' 
        CREATE TABLE IF NOT EXISTS measurehour (
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            kw          REAL NOT NULL,
            kwh         REAL NOT NULL,
            uploaded    INTERGER NOT NULL DEFAULT 0
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
        lt = time.localtime()
        print('localtime: {}'.format(lt))


        c = self.dbconn.cursor()
        #starttimestring = '{}-{}-{} {}:00:00'.format(lt.tm_year, lt.mon, lt.tm_mday, lt.tm_hour)
        #endtimestring = '{}-{}-{} {}:59:59'.format(lt.tm_year, lt.mon, lt.tm_mday, lt.tm_hour)
        starttimestring = '2018-08-01 09:00:00'
        endtimestring = '2018-08-01 09:59:59'
        sql = "select avg(kw), avg(kw) from measure where datetime between '?' and '?' and mid == ?" 
        c.excute(sql,(starttimestring, endtimestring, str(1)))

        print(c.fetchone())


        pass






if __name__ == '__main__':

    dbconn = sqlite3.connect('data.db')

    c = dbconn.cursor()



    # get how many machine id in database
    sql = "select distinct mid from measure"
    c.execute(sql)
    rows = c.fetchall()
    machines = [r[0] for r in rows]
    print(machines)




    # calculate houely values
    lt = time.localtime()
    starttimestring = '{:0=4}-{:0=2}-{:0=2} {:0=2}:00:00'.format(lt.tm_year, lt.tm_mon, lt.tm_mday, 9)
    endtimestring   = '{:0=4}-{:0=2}-{:0=2} {:0=2}:59:59'.format(lt.tm_year, lt.tm_mon, lt.tm_mday, 9)
    print(starttimestring)
    print(endtimestring)
    sql = "select avg(kw), avg(kw) from measure where datetime between ? and ? and mid == ?" 
    c.execute(sql,(starttimestring, endtimestring, '1'))
    r = c.fetchone()
    print(r)





