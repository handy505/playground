#!/usr/bin/env python3
import threading
import time
import queue
import sqlite3
import random

class Collector(threading.Thread):
    def __init__(self, dbconn):
        threading.Thread.__init__(self)       

    def run(self):
        conn = sqlite3.connect('data.db')
        while True:
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
    def __init__(self, dbconn):
        threading.Thread.__init__(self)       
        self.dbconn = dbconn

    def run(self):
        while True:
            print('uploader {}'.format(time.time()))
            time.sleep(1)

def main():

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    sql = ''' 
    CREATE TABLE IF NOT EXISTS measure (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATETIME TEXT NOT NULL,
        WATT REAL NOT NULL,
        KWH REAL NOT NULL,
        UPLOADED INTERGER NOT NULL DEFAULT 0
    );
    '''
    c.execute(sql)


    c = Collector(conn)
    u = Uploader(conn)
    c.start()
    u.start()




if __name__ == '__main__':
    main()
