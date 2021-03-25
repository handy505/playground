#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import queue
import random
import threading
from datetime import datetime
from collections import namedtuple


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset

class IncrementThread(threading.Thread):
    def __init__(self, counter):
        super().__init__()
        self.counter = counter

    def run(self):
        for _ in range(0,100000):
            self.counter.increment(1)



def main():

    c = Counter()

    threads = [IncrementThread(c) for _ in range(0, 6)]
    print(threads)
    #sys.exit()
    
    for t in threads:
        t.start()


    for t in threads:
        t.join()

    print(c.count)

if __name__ == '__main__':
    main()
