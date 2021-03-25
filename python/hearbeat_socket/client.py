#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys
import time

HOST = '59.127.196.135'
PORT = 9900 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    s.connect((HOST, PORT))

    last = time.time()
    
    while True:

        while time.time() - last > 1:
            last = time.time()
            s.sendall(b'reg 5cf9dd48e7ef')
            data = s.recv(1024)
            #print('Received', repr(data))
            print("{:0=12.8f}, recv, {}".format(time.time(), repr(data)))

