#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import threading

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        start = time.time()
        while time.time() - start < 3: 
            print('{}: {} execute.'.format(time.time(), self.name))
            time.sleep(1)

def main():
    thread1 = MyThread('thread1')
    thread2 = MyThread('thread2')
    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main()


'''
1621754338.6072528: thread1 execute.
1621754338.6089983: thread2 execute.
1621754339.6096752: thread1 execute.
1621754339.6101544: thread2 execute.
1621754340.6112397: thread2 execute.
1621754340.6113112: thread1 execute.
'''
