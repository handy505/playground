#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import mythread
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

    # thread - external file
    thread3 = mythread.ExternalFileThread(3, "thread-3")
    thread3.start()
    thread3.join()

    # thread - mutex lock
    for i in range(5):
        t = mythread.MutexDemoThread(i)
        t.start()


if __name__ == "__main__":
    main()


'''
pi@raspberrypi:~/demo/python/lessons/10_thread $ python3 main.py 
start 1595229891.041959
thread-3: 1595229891.042308
thread-3: 1595229892.043548
thread-3: 1595229893.044644
thread-3: 1595229894.0459774
thread-3: 1595229895.0472903
end 1595229896.0485923
0: num = 1
0: num = 2
0: num = 3
0: num = 4
0: num = 5
1: num = 6
1: num = 7
1: num = 8
1: num = 9
1: num = 10
2: num = 11
2: num = 12
2: num = 13
2: num = 14
2: num = 15
3: num = 16
3: num = 17
3: num = 18
3: num = 19
3: num = 20
4: num = 21
4: num = 22
4: num = 23
4: num = 24
4: num = 25
'''

