import sqlite3
from datetime import datetime


class DBHandler(object):
    def __init__(self, inmemory=False):
        if not inmemory: self.dbconn = sqlite3.connect('data.sqlite', check_same_thread=False, timeout=10)
        else:            self.dbconn = sqlite3.connect('file::memory:?cache=shared')
        self.create_table()


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


    def read_unuploaded_rows(self):
        with self.dbconn:
            c = self.dbconn.cursor()
            sql = '''SELECT * FROM measurements 
                     WHERE uploaded == 0 ORDER BY uid ASC LIMIT 10'''
            c.execute(sql)
            rows = c.fetchall()
            return rows


    def update_uploaded_row_by_uid(self, uid):
        with self.dbconn:
            c = self.dbconn.cursor()
            sql = '''UPDATE measurements SET uploaded = 1 
                     WHERE uid == ?'''
            c.execute(sql, (uid,))
            self.dbconn.commit()


    def update_uploaded_row_by_less_then_uid(self, uid):
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
    h = DBHandler()
    rows = h.read_unuploaded_rows()
    [print(r) for r in rows]


