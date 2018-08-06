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
    def __init__(self, ibus , obus, fbbus):
        threading.Thread.__init__(self)       
        self.ibus = ibus 
        self.obus = obus
        self.fbbus = fbbus

        self.commit_timestamp = time.time()

        self.event_uploading_uid = 0
        self.measure_uploading_uid = 0
        self.measurehour_uploading_uid = 0

    def run(self):
        '''
        tables:
            event
            measure measure_hourly
            illu    illu_hourly
            temp    temp_hourly
        '''
        self.dbconn = sqlite3.connect('data.db')

        self.create_event_table_if_not_exists()
        self.create_minute_table_if_not_exists()
        self.create_minutehour_table_if_not_exists()
        #self.create_illu_table_if_not_exists()
        #self.create_illuhour_table_if_not_exists()
        #self.create_temp_table_if_not_exists()
        #self.create_temphour_table_if_not_exists()



        # initialize event uploading uid
        self.init_event_uploading_uid()



        minutely_localtime = time.localtime()
        hourly_localtime = time.localtime()
        while True:
            try:
                self.event_operation()


                # every minute
                if time.localtime().tm_min != minutely_localtime.tm_min:
                    self.minutely_operation()
                    minutely_localtime = time.localtime()

                # every hour
                if time.localtime().tm_hour != hourly_localtime.tm_hour:
                    self.hourly_operation()
                    hourly_localtime = time.localtime()

                time.sleep(3)
            except Exception as ex:
                print(repr(ex))
                sys.exit()


    def event_operation(self):
        recs = []
        while not self.ibus.event.empty():
            rec = self.ibus.event.get()
            recs.append(rec)

        #recs.clear()


        # input to database
        for rec in recs:
            c = self.dbconn.cursor()
            sql = "INSERT INTO event VALUES (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, ?, ?, 0)"
            c.execute(sql, (rec.mid, rec.timestamp, rec.kind, rec.code, rec.stat, rec.onlinecount))


        # output to upload
        print('event uploading uid: {}'.format(self.event_uploading_uid))

        c = self.dbconn.cursor()
        sql = "select * from event where uid > ? limit 3"
        c.execute(sql,(self.event_uploading_uid,))
        rows = c.fetchall()
        [print(row) for row in rows]
        
        # if nothing get ???

        #uids = [row[0] for row in rows]
        #self.event_uploading_uid = max(uids) + 1
        maxuid = rows[-1][0]
        self.event_uploading_uid = maxuid
        print('event uploading uid: {}'.format(self.event_uploading_uid))

        dbeventrows = [DBEventRow(r) for r in rows] # create objects
        [self.obus.event.put(dbeventrow) for dbeventrow in dbeventrows] # output



        # feedback to database
        uuids = []
        while not self.fbbus.event.empty():
            uuid = self.fbbus.event.get()
            uuids.append(uuid)
        
        if uuids:
            #print('uploaded uuids: {}'.format(uuids))
            c = self.dbconn.cursor()
            sql = "update event set uploaded =1 where uid <= ?"
            c.execute(sql, (max(uuids),))



    def minutely_operation(self):
        recs = []
        while not self.ibus.measure.empty():
            rec = self.ibus.measure.get()
            recs.append(rec)

        for rec in recs:
            c = self.dbconn.cursor()
            sql = "INSERT INTO measure VALUES (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, 0)"
            c.execute(sql, (rec.mid, rec.timestamp, rec.kw, rec.kwh))

        print('Commit database')
        self.dbconn.commit()
        


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

        print('Commit database')
        self.dbconn.commit()


    def create_event_table_if_not_exists(self):
        c = self.dbconn.cursor()
        sql = ''' 
        CREATE TABLE IF NOT EXISTS event(
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            mid         INTEGER NOT NULL,
            datetime    TEXT NOT NULL,
            type        TEXT NOT NULL,
            code        INTEGER NOT NULL, 
            stat        TEXT NOT NULL,
            onlinecount INTEGER NOT NULL, 
            uploaded    INTEGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


    def create_minute_table_if_not_exists(self):
        c = self.dbconn.cursor()
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


    def create_minutehour_table_if_not_exists(self):
        c = self.dbconn.cursor()
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

    def init_event_uploading_uid(self):
        c = self.dbconn.cursor()
        sql = "select max(uid) from event where uploaded == 1"
        c.execute(sql)
        r = c.fetchone()
        print(r)
        print('init event uploading uid: {}'.format(self.event_uploading_uid))
        if r[0]:
            self.event_uploading_uid = r[0]
        else:
            self.event_uploading_uid = 0
        print('init event uploading uid: {}'.format(self.event_uploading_uid))




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


class DBEventRow(object):
    def __init__(self, row):
        self.uid = row[0]
        self.mid = row[1]
        self.timestring = row[2]
        self.kind = row[3]
        self.code = row[4]
        self.stat = row[5]
        self.onlinecount = row[6]




if __name__ == '__main__':

    #machine_ids(dbconn)

    #check_hourly_measure_table(dbconn)

    rt = RecorderDB(None, None, None)
    rt.start()
    rt.join()





    

