#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import threading
import collections
import queue
import random
'''
    b generate job
    c <- b
    c process
    c -> b

    excute:
    [b] export 96
    [c] process 96
    [c] after process 192
    [b] entrance 192
'''

class CThread(threading.Thread):
    def __init__(self, entrance, export):
        threading.Thread.__init__(self)
        self.entrance = entrance 
        self.export = export 
        self.looping = True

    def run(self):
        while self.looping:
            s = self.entrance.get()
            print('[c] process {}'.format(s))
            time.sleep(1)
            s = int(s) * 2
            print('[c] after process {}'.format(s))
            self.export.put(s)



class BThread(threading.Thread):
    def __init__(self, entrance, export):
        threading.Thread.__init__(self)
        self.entrance = entrance 
        self.export = export 
        self.looping = True

    def run(self):
        while self.looping:
            a = random.randint(0, 100)
            print('[b] export {}'.format(a))
            self.export.put(a)
            b = self.entrance.get()
            print('[b] entrance {}'.format(b))
            time.sleep(1)


class MainTask(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.looping = True

        # pipeline between collector and serverservice/bluetooth
        self.xque = queue.Queue()
        self.yque = queue.Queue()

        self.c = CThread(self.xque, self.yque)
        self.b1 = BThread(self.yque, self.xque)

    def run(self):
        self.c.start()
        self.b1.start()
        while True:
            time.sleep(1)


def main():
    mthread = MainTask()
    mthread.start()


if __name__ == "__main__":
    main()
