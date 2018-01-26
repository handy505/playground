#!/usr/bin/env python3
import sqlite3

def create():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('CREATE TABLE pvlog (ID INTEGER, BRAND TEXT, WATT INTEGER, KWH INTEGER)')
    c.execute("INSERT INTO pvlog VALUES (1, 'Ablerex', 10, 1200)")
    c.execute("INSERT INTO pvlog VALUES (2, 'Ablerex', 10, 1200)")
    c.execute("INSERT INTO pvlog VALUES (3, 'Delta', 10, 1200)")
    c.execute("INSERT INTO pvlog VALUES (4, 'Others', 10, 1200)")
    conn.commit()
    conn.close()

def main():
    #create()


    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pvlog WHERE ID=3')
    print(c.fetchone())
    print(c.fetchone())
    print(c.fetchone())
    print(c.fetchone())
    print(c.fetchone())


if __name__ == '__main__':
    main()
