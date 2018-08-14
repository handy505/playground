#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
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



        # initialize uploading uid
        self.init_event_uploading_uid()
        self.init_measure_uploading_uid()
        self.init_measurehour_uploading_uid()

        self.verify_hourly_measurement_table()

        self.informations()

        self.operation_hourly_measurements()



        minutely_datetime = datetime.datetime.now()
        hourly_datetime = datetime.datetime.now()
        while True:
            self.operation_events()
            self.operation_minutely_measurements()

            # every minute
            if datetime.datetime.now().minute != minutely_datetime.minute:
                #print('Minutely {}'.format(datetime.datetime.now()))

                # every 5 minute
                if datetime.datetime.now().minute % 5 == 0:

                    self.operation_hourly_measurements()

                    print('Commit database')
                    self.dbconn.commit()
                minutely_datetime = datetime.datetime.now()

            # every hour
            if datetime.datetime.now().hour != hourly_datetime.hour:
                #print('Hourly {}'.format(datetime.datetime.now()))
                hourly_datetime = datetime.datetime.now()

            time.sleep(3)

    def informations(self):
        c = self.dbconn.cursor()
        c.execute("select max(uid) from event where uploaded = 1")
        uploaded = c.fetchone()
        c.execute("select max(uid) from event")
        total = c.fetchone()
        print('event table uploaded: {}/{}'.format(uploaded[0], total[0]))

        c.execute("select max(uid) from measure where uploaded = 1")
        uploaded = c.fetchone()
        c.execute("select max(uid) from measure")
        total = c.fetchone()
        print('measure table uploaded: {}/{}'.format(uploaded[0], total[0]))

        c.execute("select max(uid) from measurehour where uploaded = 1")
        uploaded = c.fetchone()
        c.execute("select max(uid) from measurehour")
        total = c.fetchone()
        print('measurehour table uploaded: {}/{}'.format(uploaded[0], total[0]))


    def input_events(self):
        recs = []
        while not self.ibus.event.empty():
            rec = self.ibus.event.get()
            recs.append(rec)

        for rec in recs:
            c = self.dbconn.cursor()
            sql = "INSERT INTO event VALUES (NULL, ?, datetime(?, 'unixepoch', 'localtime'), ?, ?, ?, ?, 0)"
            c.execute(sql, (rec.mid, rec.timestamp, rec.kind, rec.code, rec.stat, rec.onlinecount))


    def output_events(self):
        c = self.dbconn.cursor()
        sql = "select * from event where uid > ? limit 10"
        c.execute(sql,(self.event_uploading_uid,))
        rows = c.fetchall()
        #[print(row) for row in rows]
        
        if rows:
            maxuid = rows[-1][0]
            self.event_uploading_uid = maxuid
            dbeventrows = [DBEventRow(r) for r in rows] # create objects
            [self.obus.event.put(dbeventrow) for dbeventrow in dbeventrows] # output
        #print('event uploading uid: {}'.format(self.event_uploading_uid))


    def feedback_events(self):
        uuids = []
        while not self.fbbus.event.empty():
            uuid = self.fbbus.event.get()
            uuids.append(uuid)
        
        if uuids:
            #print('event feedback uuids: {}'.format(uuids))
            c = self.dbconn.cursor()
            sql = "update event set uploaded = 1 where uid <= ?"
            c.execute(sql, (max(uuids),))


    def operation_events(self):
        self.input_events()
        self.output_events()
        self.feedback_events()


    def input_minutely_measurements(self):
        recs = []
        while not self.ibus.measure.empty():
            rec = self.ibus.measure.get()
            recs.append(rec)

        for rec in recs:
            c = self.dbconn.cursor()
            sql = "insert into measure values(NULL, ?, datetime(?, 'unixepoch', 'localtime'),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)"
            c.execute(sql, (
                rec.mid, rec.timestamp, 
                rec.OutputPower, 
                rec.ACVolPhaseA, rec.ACVolPhaseB, rec.ACVolPhaseC,
                rec.ACFrequency,
                rec.ACOutputCurrentA, rec.ACOutputCurrentB, rec.ACOutputCurrentC,
                rec.DC1InputVol, rec.DC2InputVol,
                rec.DC1InputCurrent, rec.DC2InputCurrent,
                rec.DCBusPositiveVol, rec.DCBusNegativeVol,
                rec.InternalTemper, rec.HeatSinkTemper,
                rec.InputPowerA, rec.InputPowerB,
                rec.TotalOutputPower))


    def output_minutely_measurements(self):
        c = self.dbconn.cursor()
        sql = "select * from measure where uid > ? limit 3"
        c.execute(sql,(self.measure_uploading_uid,))
        rows = c.fetchall()
        #[print(row) for row in rows]
        
        # if nothing get ???
        if rows:
            maxuid = rows[-1][0]
            self.measure_uploading_uid = maxuid
            records = [DBMeasureRow(r) for r in rows] # create objects
            [self.obus.measure.put(record) for record in records] # output
        #print('measure uploading uid: {}'.format(self.measure_uploading_uid))


    def feedback_minutely_measurements(self):
        uuids = []
        while not self.fbbus.measure.empty():
            uuid = self.fbbus.measure.get()
            uuids.append(uuid)
        
        if uuids:
            #print('uploaded uuids: {}'.format(uuids))
            c = self.dbconn.cursor()
            sql = "update measure set uploaded = 1 where uid <= ?"
            c.execute(sql, (max(uuids),))


    def operation_minutely_measurements(self):
        self.input_minutely_measurements()
        self.output_minutely_measurements()
        self.feedback_minutely_measurements()

    def operation_hourly_measurements(self):
        self.input_hourly_measurements()
        self.output_hourly_measurements()
        self.feedback_hourly_measurements()


    def input_hourly_measurements(self):
        now = datetime.datetime.now()
        dt = datetime.datetime.now() - datetime.timedelta(hours=1)
        since = '{:0=4}-{:0=2}-{:0=2} {:0=2}:00:00'.format(dt.year, dt.month, dt.day, dt.hour)
        to    = '{:0=4}-{:0=2}-{:0=2} {:0=2}:59:59'.format(dt.year, dt.month, dt.day, dt.hour)

        if self.is_hourly_row_exist(since):
            #print('{} exist, skip'.format(since))
            return 

        mids = self.get_mids(since, to)
        #print('mids: {}, {}, {}'.format(mids, since, to))
        for mid in mids:
            self.insert_one_hourly_record(since, to, mid)

        print('Commit database')
        self.dbconn.commit()


    def output_hourly_measurements(self):
        c = self.dbconn.cursor()
        sql = "select * from measurehour where uid > ? limit 3"
        c.execute(sql,(self.measurehour_uploading_uid,))
        rows = c.fetchall()
        #[print(row) for row in rows]
        
        if rows:
            maxuid = rows[-1][0]
            self.measurehour_uploading_uid = maxuid
            records = [DBMeasureHourRow(r) for r in rows] # create objects
            [self.obus.measurehour.put(record) for record in records] # output


    def feedback_hourly_measurements(self):
        uuids = []
        while not self.fbbus.measurehour.empty():
            uuid = self.fbbus.measurehour.get()
            uuids.append(uuid)
        
        if uuids:
            #print('uploaded uuids: {}'.format(uuids))
            c = self.dbconn.cursor()
            sql = "update measurehour set uploaded = 1 where uid <= ?"
            c.execute(sql, (max(uuids),))



    def get_oldest_datetime_from_minute_table(self):
        c = self.dbconn.cursor()
        sql = "select min(datetime) from measure"
        c.execute(sql)
        r = c.fetchone()
        timestring = r[0]
        return datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
        

    def get_newest_datetime_from_minute_table(self):
        c = self.dbconn.cursor()
        sql = "select max(datetime) from measure"
        c.execute(sql)
        r = c.fetchone()
        timestring = r[0]
        return datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')


    def get_hourly_datetimes(self):
        c = self.dbconn.cursor()
        sql = "select distinct(datetime) from measurehour"
        c.execute(sql)
        rows = c.fetchall()
        hourlyrecords = [r[0] for r in rows]
        #[print(hr) for hr in hourlyrecords]
        return hourlyrecords
    

    def is_hourly_row_exist(self, timestring):
        c = self.dbconn.cursor()
        sql = "select * from measurehour where datetime == ?"
        c.execute(sql, (timestring,))
        rows = c.fetchall()
        #print('rows: {}'.format(rows))
        return bool(rows)


    def get_last_kwh(self, timestring, mid):
        #print(timestring)

        c = self.dbconn.cursor()
        sql = "select max(datetime), TotalOutputPower from measurehour where datetime < ? and mid == ?"
        c.execute(sql, (timestring, mid))
        row = c.fetchone()
        #print('last kwh: {}'.format(row))
        return row[1]


    def generate_avg_measurement(self, since, to, mid):
        c = self.dbconn.cursor()
        sql = """select mid, avg(OutputPower), 
                 avg(ACVolPhaseA), avg(ACVolPhaseB), avg(ACVolPhaseC),
                 avg(ACFrequency), 
                 avg(ACOutputCurrentA), avg(ACOutputCurrentB), avg(ACOutputCurrentC),
                 avg(DC1InputVol), avg(DC2InputVol), 
                 avg(DC1InputCurrent), avg(DC2InputCurrent), 
                 avg(DCBusPositiveVol), avg(DCBusNegativeVol),
                 avg(InternalTemper), avg(HeatSinkTemper),
                 avg(InputPowerA), avg(InputPowerB),
                 max(TotalOutputPower)
                 from measure where datetime between ? and ? and mid == ?""" 
        c.execute(sql,(since, to, mid))
        avgrow = c.fetchone()

        if not avgrow[0]:
            return 

        # insert timestamp
        timestamp = time.mktime(datetime.datetime.strptime(since, '%Y-%m-%d %H:%M:%S').timetuple())
        fullrow = list(avgrow)
        fullrow.insert(1, timestamp)
        return fullrow


    def verify_hourly_measurement_table(self):

        oldest = self.get_oldest_datetime_from_minute_table()
        #print('oldest: {}'.format(oldest))
        if not oldest: 
            return

        newest = self.get_newest_datetime_from_minute_table()
        #print('newest: {}'.format(newest))
        if not newest: 
            return

        saved_hours = self.get_hourly_datetimes()
        #print('saved hours: {}'.format(saved_hours))

        oldest_hour = datetime.datetime(oldest.year, oldest.month, oldest.day, oldest.hour)
        newest_hour = datetime.datetime(newest.year, newest.month, newest.day, newest.hour) - datetime.timedelta(hours=1)
        #print('oldest hour: {}'.format(oldest_hour))
        #print('newest hour: {}'.format(newest_hour))
        dt = oldest_hour 
        h = 0
        while dt < newest_hour:
            dt = oldest_hour + datetime.timedelta(hours=h)
            since = '{:0=4}-{:0=2}-{:0=2} {:0=2}:00:00'.format(dt.year, dt.month, dt.day, dt.hour)
            to    = '{:0=4}-{:0=2}-{:0=2} {:0=2}:59:59'.format(dt.year, dt.month, dt.day, dt.hour)
            h += 1

            if self.is_hourly_row_exist(since):
                #print('{} exist, skip'.format(since))
                continue

            mids = self.get_mids(since, to)
            #print('mids: {}, {}, {}'.format(mids, since, to))
            for mid in mids:
                self.insert_one_hourly_record(since, to, mid)

        self.dbconn.commit()

    def get_mids(self, since, to):
        c = self.dbconn.cursor()
        sql = "select distinct(mid) from measure where datetime between ? and ?"
        c.execute(sql,(since, to))
        rows = c.fetchall()
        result = [row[0] for row in rows]
        return result 


    def insert_one_hourly_record(self, since, to, mid):
        row = self.generate_avg_measurement(since, to, mid)
        prevkwh = self.get_last_kwh(since, mid)
        if not prevkwh:
            prevkwh = 0

        if row:
            kwh = row[-1]
            diff = kwh - prevkwh
            if diff < 0: 
                diff = 0

            #print('KWH: {}, prev: {}, diff: {}'.format(kwh, prevkwh, diff))
            row.append(prevkwh)
            row.append(diff)
            c = self.dbconn.cursor()
            sql = "insert into measurehour values(NULL, ?, datetime(?, 'unixepoch', 'localtime'),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)"
            c.execute(sql, row)


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
            uid                 INTEGER PRIMARY KEY AUTOINCREMENT,
            mid                 INTEGER NOT NULL,
            datetime            TEXT NOT NULL,
            OutputPower         REAL NOT NULL,
            ACVolPhaseA         INTEGER NOT NULL,
            ACVolPhaseB         INTEGER NOT NULL,
            ACVolPhaseC         INTEGER NOT NULL,
            ACFrequency         REAL NOT NULL,
            ACOutputCurrentA    REAL NOT NULL,
            ACOutputCurrentB    REAL NOT NULL,
            ACOutputCurrentC    REAL NOT NULL,
            DC1InputVol         REAL NOT NULL,
            DC2InputVol         REAL NOT NULL,
            DC1InputCurrent     REAL NOT NULL,
            DC2InputCurrent     REAL NOT NULL,
            DCBusPositiveVol    INTEGER NOT NULL,
            DCBusNegativeVol    INTEGER NOT NULL,
            InternalTemper      INTEGER NOT NULL,
            HeatSinkTemper      INTEGER NOT NULL,
            InputPowerA         REAL NOT NULL,
            InputPowerB         REAL NOT NULL,
            TotalOutputPower    INTEGER NOT NULL,
            uploaded            INTEGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


    def create_minutehour_table_if_not_exists(self):
        c = self.dbconn.cursor()
        sql = ''' 
        CREATE TABLE IF NOT EXISTS measurehour (
            uid                  INTEGER PRIMARY KEY AUTOINCREMENT,
            mid                  INTEGER NOT NULL,
            datetime             TEXT NOT NULL,
            OutputPower          REAL NOT NULL,
            ACVolPhaseA          REAL NOT NULL,
            ACVolPhaseB          REAL NOT NULL,
            ACVolPhaseC          REAL NOT NULL,
            ACFrequency          REAL NOT NULL,
            ACOutputCurrentA     REAL NOT NULL,
            ACOutputCurrentB     REAL NOT NULL,
            ACOutputCurrentC     REAL NOT NULL,
            DC1InputVol          REAL NOT NULL,
            DC2InputVol          REAL NOT NULL,
            DC1InputCurrent      REAL NOT NULL,
            DC2InputCurrent      REAL NOT NULL,
            DCBusPositiveVol     REAL NOT NULL,
            DCBusNegativeVol     REAL NOT NULL,
            InternalTemper       REAL NOT NULL,
            HeatSinkTemper       REAL NOT NULL,
            InputPowerA          REAL NOT NULL,
            InputPowerB          REAL NOT NULL,
            TotalOutputPower     REAL NOT NULL,
            PrevTotalOutputPower REAL NOT NULL,
            DiffTotalOutputPower REAL NOT NULL,
            uploaded             INTEGER NOT NULL DEFAULT 0
        );
        '''
        c.execute(sql)


    def init_event_uploading_uid(self):
        c = self.dbconn.cursor()
        sql = "select max(uid) from event where uploaded == 1"
        c.execute(sql)
        r = c.fetchone()
        if r[0]:
            self.event_uploading_uid = r[0]
        else:
            self.event_uploading_uid = 0
        #print('Init event uploading uid: {}'.format(self.event_uploading_uid))


    def init_measure_uploading_uid(self):
        c = self.dbconn.cursor()
        sql = "select max(uid) from measure where uploaded == 1"
        c.execute(sql)
        r = c.fetchone()
        if r[0]: 
            self.measure_uploading_uid = r[0]
        else:    
            self.measure_uploading_uid = 0
        #print('Init measure uploading uid: {}'.format(self.measure_uploading_uid))


    def init_measurehour_uploading_uid(self):
        c = self.dbconn.cursor()
        sql = "select max(uid) from measurehour where uploaded == 1"
        c.execute(sql)
        r = c.fetchone()
        if r[0]: 
            self.measurehour_uploading_uid = r[0]
        else:    
            self.measurehour_uploading_uid = 0
        #print('Init measurehour uploading uid: {}'.format(self.measurehour_uploading_uid))


class DBEventRow(object):
    def __init__(self, row):
        self.uid = row[0]
        self.mid = row[1]
        self.timestring = row[2]
        self.event_type = row[3]
        self.event_index = row[4]
        self.event_parameter = row[5]
        self.inverter_good = row[6]


class DBMeasureRow(object):
    def __init__(self, row):
        self.uid = row[0]
        self.mid = row[1]
        self.timestring = row[2]
        self.OutputPower = row[3]
        self.ACVolPhaseA = row[4]
        self.ACVolPhaseB = row[5]
        self.ACVolPhaseC = row[6]
        self.ACFrequency = row[7]
        self.ACOutputCurrentA = row[8]
        self.ACOutputCurrentB = row[9]
        self.ACOutputCurrentC = row[10]
        self.DC1InputVol = row[11]
        self.DC2InputVol = row[12]
        self.DC1InputCurrent = row[13]
        self.DC2InputCurrent = row[14]
        self.DCBusPositiveVol = row[15]
        self.DCBusNegativeVol = row[16]
        self.InternalTemper = row[17]
        self.HeatSinkTemper = row[18]
        self.InputPowerA = row[19]
        self.InputPowerB = row[20]
        self.TotalOutputPower = row[21]


class DBMeasureHourRow(object):
    def __init__(self, row):
        self.uid = row[0]
        self.mid = row[1]
        self.timestring = row[2]
        self.OutputPower = row[3]
        self.ACVolPhaseA = row[4]
        self.ACVolPhaseB = row[5]
        self.ACVolPhaseC = row[6]
        self.ACFrequency = row[7]
        self.ACOutputCurrentA = row[8]
        self.ACOutputCurrentB = row[9]
        self.ACOutputCurrentC = row[10]
        self.DC1InputVol = row[11]
        self.DC2InputVol = row[12]
        self.DC1InputCurrent = row[13]
        self.DC2InputCurrent = row[14]
        self.DCBusPositiveVol = row[15]
        self.DCBusNegativeVol = row[16]
        self.InternalTemper = row[17]
        self.HeatSinkTemper = row[18]
        self.InputPowerA = row[19]
        self.InputPowerB = row[20]
        self.TotalOutputPower = row[21]
        self.PrevTotalOutputPower = row[22]
        self.DiffTotalOutputPower = row[23]

if __name__ == '__main__':

    #machine_ids(dbconn)


    rt = RecorderDB(None, None, None)
    rt.start()
    rt.join()


