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
            print('\t[server recv] ' + s)


HOST = 'localhost'
PORT = 12345

#commands = ['ifconfig wlan0', 'hostname', 'date']
commands = ['hostname', 'date']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
    so.bind((HOST, PORT))
    so.listen(1)
    conn, addr = so.accept()
    try:
        with conn:
            print('Connected by', addr)
            
            
            rt = threading.Thread(target=recv_process, args=(conn, addr))
            rt.start()
            
            while True:
                
                s = commands[random.randint(0, len(commands)-1)]
                bs = bytearray(s.encode('utf-8'))
                conn.sendall(bs)
                print('[server send]' + bs.decode('utf-8'))

                time.sleep(2)
        

    except socket.error as err:
        print(err)
    except OSError as err:
        print(err)
    finally:
        conn.close()





                

