#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import myfunc
from uuid import getnode
import time
import math
import threading
import myobj
import mythread

def add(arg1, arg2):
    return arg1 + arg2


exit_flag = 0


class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("starting {0}".format(self.name))
        print_time(self.name, self.counter, 5)
        print("exiting {0}".format(self.name))


def print_time(thread_name, delay, counter):
    while counter:
        print("{0}: {1}".format(thread_name, time.ctime(time.time())))
        counter -= 1
        if exit_flag:
            thread_name.exit()
        time.sleep(delay)


def main():

    print("hello python")

    # function call
    var1 = add(2, 3)
    print("current file function call: " + str(var1))

    # cross file function call
    var2 = myfunc.add(1, 2)
    print("cross file function call: " + str(var2))

    # timestamp
    now = time.time()
    print("now in seconds: " + str(now))
    timearr = time.localtime(now)
    print("hour: {0}, minute: {1}, seconds: {2}".format(
        timearr.tm_hour, timearr.tm_min, timearr.tm_sec))

    # hardware, mac address
    mac = hex(getnode())
    print("mac: " + mac)

    # file1
    fout = open("abc.txt", "w", encoding="utf-8")
    fout.write("abcdefg\n")
    fout.close()

    # file2
    with open("def.txt", "w", encoding="utf-8") as fh:
        fh.write("abcdefghijk\n")

    # perfermence
    t1 = time.clock()
    ans = math.sqrt(2)
    t2 = time.clock()
    print("sqrt(2) = {0}, elapse time: {1}".format(ans, t2-t1))

    # object
    c = myobj.Circle()
    print("area = {0}".format(c.area))

    # thread
    thread1 = MyThread(1, "thread1", 1)
    thread2 = MyThread(2, "thread2", 2)

    thread1.start()
    thread2.start()

    print("start join: {}".format(time.time()))
    thread1.join()
    thread2.join()
    print("end join: {}".format(time.time()))


    # thread2
    ptask = mythread.PollingThread(3, "thread3", 3)
    ptask.start()
    ptask.join()

if __name__ == "__main__":
    main()
