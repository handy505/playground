#!/usr/bin/env python3
import time
import threading
import sqlite3
from datetime import datetime


class UploaderThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.dbconn = sqlite3.connect('data.sqlite', check_same_thread=False, timeout=10)
        self.uid = 0


    def run(self):
        while True:
            with self.dbconn:
                #self.mutex.acquire(1)
                rows = self.fetch_from_database()
                #self.mutex.release()

            print('---------------------')
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





if __name__ == '__main__':
    ut = UploaderThread()
    ut.start()
