#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys

HOST = "localhost"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            #if not data: break
            if data:
                print(data)
                conn.sendall(data)
