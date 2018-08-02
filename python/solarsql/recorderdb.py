#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
import random
import queue
import sys
import os
import datetime


class RecorderDB(threading.Thread):
    def __init__(self, ibus , oqueue, fbqueue):
        threading.Thread.__init__(self)       
        self.ibus = ibus 
        self.oqueue = oqueue
        self.fbqueue = fbqueue

        self.commit_timestamp = time.time()

    def run(self):
        '''
        tables:
            event
            measure measure_hourly
            illu    illu_hourly
            temp    temp_hourly
        '''
        self.dbconn = sqlite3.connect('data.db')
        c = self.dbconn.cursor()


        # create event table
        sql = ''' 
        CREATE TABLE IF NOT EXISTS event(
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            older       INTEGER NOT NULL,
            newer       INTEGER NOT NULL,
            uploaded    INTEGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


        # create measure table
        sql = ''' 
        CREATE TABLE IF NOT EXISTS measure (
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            kw          REAL NOT NULL,
            kwh         REAL NOT NULL,
            uploaded    INTEGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


        # create hourly measure table
        sql = ''' 
        CREATE TABLE IF NOT EXISTS measurehour (
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            kw          REAL NOT NULL,
            kwh         REAL NOT NULL,
            uploaded    INTEGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)

        minutely_localtime = time.localtime()
        hourly_localtime = time.localtime()

        while True:
            try:

                # every minute
                if time.localtime().tm_min != minutely_localtime.tm_min:
                    self.event_operation()
                    self.minutely_operation()
                    minutely_localtime = time.localtime()


                # every hour
                if time.localtime().tm_hour != hourly_localtime.tm_hour:
                    self.hourly_operation()
                    hourly_localtime = time.localtime()


                time.sleep(3)
            except Exception as ex:
                print(repr(ex))
                cmd = 'echo {} >> recorderdb.log'.format(repr(ex))
                os.system(cmd)

    def event_operation(self):
        recs = []
        while not self.ibus.event.empty():
            rec = self.ibus.event.get()
            recs.append(rec)

        print('receive {} events'.format(len(recs)))





    def minutely_operation(self):
        recs = []
        while not self.ibus.measure.empty():
            rec = self.ibus.measure.get()
            recs.append(rec)


        start  = time.time()
        for rec in recs:
            c = self.dbconn.cursor()
            sql = "INSERT INTO measure VALUES (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, 0)"
            c.execute(sql, (rec.mid, rec.timestamp, rec.kw, rec.kwh))
        print('Insert database: {} seconds'.format(round((time.time()-start),6)))


        # commit
        if time.time() - self.commit_timestamp > (60*10):
            start = time.time()
            self.dbconn.commit()
            print('Commit database: {} seconds'.format(round((time.time()-start),6)))
            self.commit_timestamp = time.time()


    def hourly_operation(self):
        print('hour_operation()')

        now = datetime.datetime.now()
        start = '{:0=4}-{:0=2}-{:0=2} {:0=2}:00:00'.format(now.year, now.month, now.day, now.hour)
        end   = '{:0=4}-{:0=2}-{:0=2} {:0=2}:59:59'.format(now.year, now.month, now.day, now.hour)
        
        c = self.dbconn.cursor()
        sql = "select avg(kw), avg(kwh) from measure where datetime between ? and ? and mid == ?" 
        c.execute(sql,(start, end, '1'))
        r = c.fetchone()
        kw = r[0]
        kwh = r[1]
        if kw and kwh:
            mid = 1
            hourdt = now + datetime.timedelta(hours=1)
            timestamp = time.mktime(hourdt.timetuple())
            sql = "insert into measurehour values (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, 0)"
            c.execute(sql, (mid, timestamp, kw, kwh))

        self.dbconn.commit()
        print('Commit database')




def check_hourly_measure_table(dbconn):
    c = dbconn.cursor()

    # get last minute time string
    sql = "select min(datetime) from measure"
    c.execute(sql)
    r = c.fetchone()
    timestring = r[0]
    oldest= datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')


    sql = "select max(datetime) from measure"
    c.execute(sql)
    r = c.fetchone()
    timestring = r[0]
    newest= datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
    print('oldest: {}'.format(repr(oldest)))
    print('newest: {}'.format(repr(newest)))


    sql = "select distinct(datetime) from measurehour"
    c.execute(sql)
    rows = c.fetchall()
    hourlyrecords = [r[0] for r in rows]
    [print(hr) for hr in hourlyrecords]

    since = datetime.datetime(oldest.year, oldest.month, oldest.day, oldest.hour)
    dt = since
    h = 0
    while dt < newest:
        dt = since + datetime.timedelta(hours=h)

        # calculate avg
        start = '{:0=4}-{:0=2}-{:0=2} {:0=2}:00:00'.format(dt.year, dt.month, dt.day, dt.hour)
        end   = '{:0=4}-{:0=2}-{:0=2} {:0=2}:59:59'.format(dt.year, dt.month, dt.day, dt.hour)
        sql = "select avg(kw), avg(kwh) from measure where datetime between ? and ? and mid == ?" 
        c.execute(sql,(start, end, '1'))
        r = c.fetchone()
        print(r)

        kw = r[0]
        kwh = r[1]
        hourdt = dt + datetime.timedelta(hours=1)
        if kw and kwh and (str(hourdt) not in hourlyrecords):
            mid = 1
            timestamp = time.mktime(hourdt.timetuple())
            sql = "insert into measurehour values (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, 0)"
            c.execute(sql, (mid, timestamp, kw, kwh))

        h += 1

    dbconn.commit()


def machine_ids(dbconn):
    # get how many machine id in database
    sql = "select distinct mid from measure"
    c.execute(sql)
    rows = c.fetchall()
    machines = [r[0] for r in rows]
    print(machines)


if __name__ == '__main__':

    dbconn = sqlite3.connect('data.db')


    #machine_ids(dbconn)

    #check_hourly_measure_table(dbconn)








    

