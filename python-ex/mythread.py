#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import threading


class PollingThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        start = time.time()
        print("start {0}".format(start))

        while time.time() - start < 5:
            print("polling at {0}".format(time.time()))
            time.sleep(1)

        print("end {0}".format(time.time()))


if __name__ == "__main__":
    pass
