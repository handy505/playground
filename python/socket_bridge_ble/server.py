#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import sys
import time
import random
import threading

def recv_process(conn, addr):
    while(True):
        data = conn.recv(1024)
        if data:
            s = data.decode('utf-8')
            print('\t' + s)


HOST = 'localhost'
PORT = 12345

commands = ['ifconfig wlan0', 'hostname', 'date']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
    so.bind((HOST, PORT))
    so.listen(1)
    conn, addr = so.accept()
    try:
        with conn:
            print('Connected by', addr)
            
            
            rt = threading.Thread(target=recv_process, args=(conn, addr))
            rt.start()
            last = time.time()
            while True:
                
                if time.time() - last > 3:
                    '''ts = time.strftime('%H:%M:%S', time.localtime(round(time.time())))
                    s = ts + ' ' + commands[random.randint(0,2)]'''
                    bs = bytearray(s.encode('utf-8'))
                    conn.sendall(bs)
                    print(ts)
                    last = time.time()

                    '''data = conn.recv(1024)
                    if data:
                        s = data.decode('utf-8')
                        print('\t' + s)'''

    except socket.error as err:
        print(err)
    except OSError as err:
        print(err)
    finally:
        conn.close()





                

