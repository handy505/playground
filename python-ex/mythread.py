#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import threading


class ExternalFileThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        start = time.time()
        print("start {0}".format(start))

        while time.time() - start < 5:
            print("{0}: {1}".format(self.name, time.time()))
            time.sleep(1)

        print("end {0}".format(time.time()))


num = 0
mutex = threading.Lock()


class MutexDemoThread(threading.Thread):
    def __init__(self, threadID=0, name="thread0"):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global num
        if mutex.acquire(1):  # get mutex lock
            tmp = num
            tmp += 1
            time.sleep(1)
            num = tmp 
            print("{0}: num = {1}".format(self.threadID, num))
            mutex.release()  # release mutex lock


if __name__ == "__main__":
    pass
