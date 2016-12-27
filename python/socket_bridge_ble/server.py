#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys
import time
import random

HOST = 'localhost'
PORT = 12345

commands = ['ifconfig wlan0', 'hostname', 'date']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    try:
        with conn:
            print('Connected by', addr)

            last = time.time()
            while True:
                
                while time.time() - last > 3:
                    ts = time.strftime('%H:%M:%S', time.localtime(round(time.time())))
                    ts = ts + ' ' + commands[random.randint(0,2)]
                    bs = bytearray(ts.encode('utf-8'))
                    conn.sendall(bs)
                    print(ts)
                    last = time.time()

    except socket.error as err:
        print(err)
    finally:
        conn.close()



