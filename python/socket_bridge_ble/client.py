#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys
import time

HOST = 'localhost'
PORT = 12345
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:

    so.connect((HOST, PORT))

    while True:


        data = so.recv(1024)
        if data:
            s = data.decode('utf-8')
            print('\t' + s)

            s = 'response data'
            bs = bytearray(s.encode('utf-8'))
            so.sendall(bs)
            print(s)