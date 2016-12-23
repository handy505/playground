#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys
import time

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        '''while True:
            data = conn.recv(1024)
            #if not data: break
            if data:
                print(data)
                conn.sendall(data)'''

        last = time.time()
        while True:
            
            while time.time() - last > 3:
                ts = time.strftime('%H:%M:%S', time.localtime(round(time.time())))
                bs = bytearray(ts.encode('utf-8'))
                conn.sendall(bs)
                print(ts)
                last = time.time()



