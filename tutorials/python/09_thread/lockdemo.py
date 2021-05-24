#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import threading

class MyThread(threading.Thread):
    def __init__(self, name, lock):
        threading.Thread.__init__(self)

        self.lock = lock
        self.name = name
        self.chars = [c for c in self.name]

    def run(self):
        while True:
            with self.lock:
                for c in self.chars:
                    print(c)
                    time.sleep(0.1)
            time.sleep(0.1)

def main():
    lock = threading.RLock()
    th1 = MyThread('123', lock)
    th2 = MyThread('ABC', lock)
    th1.start()
    th2.start()


if __name__ == "__main__":
    main()


