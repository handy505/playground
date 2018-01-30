#!/usr/bin/env python3
import sqlite3
import pathlib
import os


def create():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    sql = '''
    CREATE TABLE mytable(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATETIME TEXT,
        TEMP REAL,
        UARTCLK INTEGER)''' 
    c.execute(sql)
    conn.commit()
    conn.close()

def main():
    f = pathlib.Path('data.db')
    if not f.exists():
        create()

    '''
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pvlog WHERE ID=3')
    print(c.fetchone())
    print(c.fetchone())
    print(c.fetchone())
    print(c.fetchone())
    print(c.fetchone())
    '''

    ret = os.popen('vcgencmd measure_temp').read()
    temperature = ret.split('=')[1]
    temperature = temperature[:-3]
    print(temperature)

    ret = os.popen('vcgencmd measure_clock uart').read()
    clock = ret.split('=')[1]
    print(clock)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO mytable VALUES (NULL, datetime('now', 'localtime'), ?, ?)", (temperature, clock))
    conn.commit()
    




if __name__ == '__main__':
    main()
