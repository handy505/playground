#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import threading

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

    # thread - normal
    thread1 = MyThread(1, "thread-1", 1)
    thread2 = MyThread(2, "thread-2", 2)

    thread1.start()
    thread2.start()

    print("start join: {0}".format(time.time()))
    thread1.join()
    thread2.join()
    print("end join: {0}".format(time.time()))


if __name__ == "__main__":
    main()


'''
pi@raspberrypi:~/demo/python/lessons $ python3 09_thread.py 
starting thread-1
thread-1: Mon Jul 20 15:20:39 2020
starting thread-2
start join: 1595229639.8829954
thread-2: Mon Jul 20 15:20:39 2020
thread-1: Mon Jul 20 15:20:40 2020
thread-1: Mon Jul 20 15:20:41 2020
thread-2: Mon Jul 20 15:20:41 2020
thread-1: Mon Jul 20 15:20:42 2020
thread-1: Mon Jul 20 15:20:43 2020
thread-2: Mon Jul 20 15:20:43 2020
exiting thread-1
thread-2: Mon Jul 20 15:20:45 2020
thread-2: Mon Jul 20 15:20:47 2020
exiting thread-2
end join: 1595229649.8949854
'''
