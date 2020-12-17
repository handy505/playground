#!/usr/bin/env python3
import threading
import time
import queue
import sys
from datetime import datetime
from collections import namedtuple
import sqlite3
import random

Record = namedtuple('Record', ['deviceid', 'loggeddatetime', 'kw', 'kwh'])

class Inverter(object):
    def __init__(self, id):
        self.id = id
        self.kw = 52
        self.kwh = 100
    
    def __str__(self):
        return 'Inverter-{}'.format(self.id)

    def get_record(self):
        return Record(self.id, datetime.now(), self.kw, self.kwh)


class Collector(threading.Thread):
    def __init__(self, mutex):
        threading.Thread.__init__(self)       

        self.mutex = mutex 
        self.dbconn = sqlite3.connect('data.sqlite', check_same_thread=False, timeout=10)

        with self.mutex:
            self.create_table()


    def run(self):
        inverters = [Inverter(i) for i in range(1,3)]
        [print(pv) for pv in inverters]

        while True:
            for inv in inverters:
                rec = inv.get_record()
                print(rec)

                with self.dbconn:
                    #self.mutex.acquire(1)
                    self.output_to_database(rec)
                    #self.mutex.release()


            time.sleep(1)

            with self.dbconn:
                #self.mutex.acquire(1)
                self.dbconn.commit()
                #self.mutex.release()


    def output_to_database(self, rec):
        c = self.dbconn.cursor()
        sql = """INSERT INTO measurements 
                 VALUES(NULL, ?, ?, ?, ?, 0)"""
        c.execute(sql, (rec.deviceid,
                        str(rec.loggeddatetime.replace(microsecond=0)), 
                        rec.kw, 
                        rec.kwh)) 


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


class Uploader(threading.Thread):
    def __init__(self, mutex):
        threading.Thread.__init__(self)       
        self.mutex = mutex 
        self.dbconn = sqlite3.connect('data.sqlite', check_same_thread=False, timeout=10)
        self.uid = 0

    def run(self):
        while True:
            with self.dbconn:
                #self.mutex.acquire(1)
                rows = self.fetch_from_database()
                #self.mutex.release()

            [print(row) for row in rows]

            self.uid = rows[-1][0]


            with self.dbconn:
                #self.mutex.acquire(1)
                self.update()
                #self.mutex.release()

            time.sleep(1)



    def fetch_from_database(self):
        c = self.dbconn.cursor()
        sql = """SELECT * FROM measurements 
                 WHERE uid > ? LIMIT 10"""
        c.execute(sql, (self.uid,))
        rows = c.fetchall()
        return rows



    def update(self):
        c = self.dbconn.cursor()
        sql = """UPDATE measurements SET uploaded = 1 
                 WHERE uid <= ?"""
        c.execute(sql, (self.uid,))
        self.dbconn.commit()



def main():


    mutex = threading.Lock()

    ct = Collector(mutex)
    ut = Uploader(mutex)

    ct.start()
    ut.start()

    #ct.join()
    #ut.join()


if __name__ == '__main__':
    main()


