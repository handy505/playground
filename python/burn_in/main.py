#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import threading
import time


exit_flag = 0

class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("starting {0}".format(self.name))
        #print_time(self.name, self.counter, 5)
        #print("exiting {0}".format(self.name))

        while(1):
            continue

def print_time(thread_name, delay, counter):
    while counter:
        print("{0}: {1}".format(thread_name, time.ctime(time.time())))
        counter -= 1
        if exit_flag:
            thread_name.exit()
            time.sleep(delay)




def main():
    print("hello gogogo")
    # thread - normal
    thread1 = MyThread(1, "thread-1", 1)
    thread1.start()

    thread2 = MyThread(2, "thread-2", 1)
    thread2.start()

    thread3 = MyThread(3, "thread-3", 1)
    thread3.start()

    thread4 = MyThread(4, "thread-4", 1)
    thread4.start()
    
    thread5 = MyThread(5, "thread-5", 1)
    thread5.start()



    for i in range(1, 10):
        MyThread(i, "thr-" + str(i), 1).start()



    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

if __name__ == "__main__":
    main()

