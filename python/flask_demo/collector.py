#!/usr/bin/env python3
import time
import threading
import sqlite3
from datetime import datetime

class CollectorThread(threading.Thread):
    def __init__(self, inverters):
        super().__init__()
        self.inverters = inverters
        self.dbconn = sqlite3.connect('data.sqlite', check_same_thread=False, timeout=10)
        self.create_table()

        self.datetime_of_output_action = datetime.now()

    def run(self):
        while True:
            for inv in self.inverters:
                #print(inv)
                inv.sync_with_hardware()


            
            # every minute
            if datetime.now().minute != self.datetime_of_output_action.minute:

                with self.dbconn:
                    for inv in self.inverters:
                        #self.mutex.acquire(1)
                        rec = inv.get_record()
                        self.output_to_database(rec)
                        #self.mutex.release()

                    self.dbconn.commit()
                    
                self.datetime_of_output_action = datetime.now()

            time.sleep(3)



    def create_table(self):
        c = self.dbconn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS measurements (
                 uid             INTEGER PRIMARY KEY AUTOINCREMENT,
                 deviceid        INTEGER NOT NULL,
                 loggeddatetime  TEXT NOT NULL,
                 kw              REAL NOT NULL,
                 kwh             INTEGER NOT NULL,
                 uploaded        INTEGER NOT NULL DEFAULT 0);'''
        c.execute(sql)


    def output_to_database(self, rec):
        c = self.dbconn.cursor()
        sql = """INSERT INTO measurements 
                 VALUES(NULL, ?, ?, ?, ?, 0)"""
        c.execute(sql, (rec.DeviceID,
                        str(rec.LoggedDatetime.replace(microsecond=0)), 
                        rec.KW, 
                        rec.KWH)) 



if __name__ == '__main__':
    
    from inverter import Inverter, Record
    inverters = [Inverter(id) for id in range(1,3)]

    while True:

        for inv in inverters:
            rec = inv.get_record()
            print(rec)

        time.sleep(1)
    




