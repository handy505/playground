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
        self.illu_uploading_uid = 0
        self.temp_uploading_uid = 0


    def run(self):
        self.dbconn = sqlite3.connect('data.sqlite')

        self.create_minute_table_if_not_exists()

        self.init_measure_uploading_uid()

        self.informations()

        minutely_datetime = datetime.datetime.now()

        while True:
            self.operation_measurements()

            # every minute
            if datetime.datetime.now().minute != minutely_datetime.minute:
                # every 5 minute
                if datetime.datetime.now().minute % 5 == 0:
                    print('Commit database')
                    self.dbconn.commit()
                minutely_datetime = datetime.datetime.now()

            time.sleep(3)


    def informations(self):
        c = self.dbconn.cursor()
        c.execute("select max(uid) from measure where uploaded = 1")
        uploaded = c.fetchone()
        c.execute("select max(uid) from measure")
        total = c.fetchone()
        print('Information of measure table uploaded: {}/{}'.format(uploaded[0], total[0]))


    def operation_measurements(self):
        self.input_measurements()
        self.output_measurements()
        self.feedback_measurements()


    def input_measurements(self):
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


    def output_measurements(self):
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


    def feedback_measurements(self):
        uuids = []
        while not self.fbbus.measure.empty():
            uuid = self.fbbus.measure.get()
            uuids.append(uuid)
        
        if uuids:
            #print('uploaded uuids: {}'.format(uuids))
            c = self.dbconn.cursor()
            sql = "update measure set uploaded = 1 where uid <= ?"
            c.execute(sql, (max(uuids),))


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



if __name__ == '__main__':
    import main

    rt = RecorderDB(main.Bus(), main.Bus(), main.Bus())
    rt.start()
    rt.join()


