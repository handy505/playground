#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import threading

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.chars = [c for c in self.name]

    def run(self):
        while True:
            for c in self.chars:
                print(c)
                time.sleep(0.1)

def main():
    th1 = MyThread('123')
    th2 = MyThread('ABC')
    th1.start()
    th2.start()


if __name__ == "__main__":
    main()


