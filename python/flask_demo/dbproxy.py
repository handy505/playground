import sqlite3
from datetime import datetime


class DBProxy(object):
    def __init__(self):
        self.dbconn = sqlite3.connect('data.sqlite', check_same_thread=False, timeout=10)


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


    def insert_record(self, rec):
        with self.dbconn:
            c = self.dbconn.cursor()
            sql = '''INSERT INTO measurements 
                     VALUES(NULL, ?, ?, ?, ?, 0)'''
            c.execute(sql, (rec.DeviceID,
                            str(rec.LoggedDatetime.replace(microsecond=0)), 
                            rec.KW, 
                            rec.KWH)) 


    def read_from_uid(self, uid):
        with self.dbconn:
            c = self.dbconn.cursor()
            sql = '''SELECT * FROM measurements 
                     WHERE uid > ? LIMIT 10'''
            c.execute(sql, (uid,))
            rows = c.fetchall()
            return rows



    def update_uploaded_by_uid(self, uid):
        with self.dbconn:
            c = self.dbconn.cursor()
            sql = '''UPDATE measurements SET uploaded = 1 
                     WHERE uid <= ?'''
            c.execute(sql, (uid,))
            self.dbconn.commit()


    def commit(self):
        with self.dbconn:
            self.dbconn.commit()


if __name__ == '__main__':

    from inverter import Inverter, Record

    p = DBProxy()

    r = Record(1, datetime.now(), 52, 200)
    p.insert_record(r)

    rows = p.read_from_uid(0)
    for r in rows:
        print(r)


