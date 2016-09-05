#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys
import time


HOST = 'localhost'
PORT = 12345
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect((HOST, PORT))

    last = time.time()
    while True:

        while time.time() - last > 1:
            last = time.time()
            s.sendall(b'hello')
            data = s.recv(1024)
            print('Received', repr(data))
