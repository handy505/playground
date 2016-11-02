#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import time
from queue import Queue


class ATask(threading.Thread):

    def __init__(self, request_queue, response_queue):
        threading.Thread.__init__(self)
        self.request_queue = request_queue
        self.response_queue = response_queue
        

    def run(self):
        #time.sleep(3)
        self.cmd = "ifconfig"
        self.request_queue.put(self.cmd)
        print("[a] {}".format(self.cmd))
        r = self.response_queue.get()
        print("[a] {}".format(r))

class BTask(threading.Thread):

    def __init__(self, request_queue, response_queue):
        threading.Thread.__init__(self)
        self.request_queue = request_queue
        self.response_queue = response_queue

    def run(self):

        while True:
            
            r = self.request_queue.get()
            print("[b] get {}".format(r))
            time.sleep(1) # simu process time
            rr = r+"-response"

            self.response_queue.put(rr)
            print("[b] put {}".format(r))


            
            



if __name__ == "__main__":

    q1 = Queue(1)
    q2 = Queue(1)

    tha = ATask(q1, q2).start()

    thb = BTask(q1, q2).start()