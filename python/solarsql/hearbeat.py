#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket
import sys 
import time
import threading
import os
import datetime


class Hearbeat(threading.Thread):
    def __init__(self):
        self.recv_data = None
        threading.Thread.__init__(self)
        self.looping = True


        # hearbeat_message format: reg <mac>
        cmd = "hciconfig | grep Address | awk {'print $3'}"
        mac = os.popen(cmd).read().strip('\n')
        mac = mac.replace(':', '')
        self.hearbeat_message = 'reg {}'.format(mac.upper())

        self.hearbeat_active_timestamp = 0
        self.recieve_data_timestamp = 0



    def run(self):

        while self.looping: 
            try:
                self.long_socket_connection()
            except (ConnectionResetError, BrokenPipeError, OSError) as ex:
                print('ex: {}'.format(repr(ex)))
            except socket.timeout as ex:
                print('ex: {}'.format(repr(ex)))
            except Exception as ex:
                print('ex: {}(NOT EXPECT !)'.format(repr(ex)))

            time.sleep(60)


    def long_socket_connection(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
            so.settimeout(30)
            so.connect(('61.216.58.150', 9900))

            while self.looping: 
                # hearbeat
                if time.time() - self.hearbeat_active_timestamp > (4*60):
                    msg = self.hearbeat_message 
                    start = datetime.datetime.now()
                    ret = so.sendall(msg.encode('utf-8'))
                    print('\thearbeat sendall: {} at {}'.format(msg, start))
                    self.recv_data = self.recv_from_socket_with_retry(so)
                    print('\thearbeat received: {} spend {}'.format(repr(self.recv_data), datetime.datetime.now()-start))
                    if self.recv_data:
                        self.hearbeat_active_timestamp = time.time()

                time.sleep(1)



    def recv_from_socket_with_retry(self, sock):
        # Workaround: Interrupted system calls
        # refer to https://www.python.org/dev/peps/pep-0475
        while True:
            try:
                result = sock.recv(1024)
                return result 
            except socket.timeout as ex:
                # resolve connection broken with server service issue
                print(repr(ex))
                break
            except InterruptedError as ex: 
                print(repr(ex))



if __name__ == '__main__':
    h = Hearbeat()
    h.start()
