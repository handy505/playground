#!/usr/bin/env python3
import sqlite3
import pathlib
import os
import optparse

def create():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    sql = '''
    CREATE TABLE temptab(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATETIME TEXT,
        TEMP REAL,
        UARTCLK INTEGER) ''' 
    c.execute(sql)
    conn.commit()
    conn.close()

def main():
    f = pathlib.Path('data.db')
    if not f.exists():
        create()

    ret = os.popen('vcgencmd measure_temp').read()
    temperature = ret.split('=')[1]
    temperature = temperature[:-3]
    print(temperature)

    ret = os.popen('vcgencmd measure_clock uart').read()
    clock = ret.split('=')[1]
    print(clock)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO temptab VALUES (NULL, datetime('now', 'localtime'), ?, ?)",
        (temperature, clock))
    conn.commit()
    


if __name__ == '__main__':
    # option parse
    parser = optparse.OptionParser()
    parser.add_option(
        '--working-dir',
        dest='workingdir',
        type='string',
        help='working path')
        
    opts, args = parser.parse_args()

    # working directory, IMPORTANT !!!
    if opts.workingdir:
        os.chdir(opts.workingdir)





    main()
