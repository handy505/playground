#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading


class SerialTask(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._name = "serial_task"
        self._sname = "[s]"

    def run(self):
        start = time.time()
        print("{} start at {}".format(self._sname, start))

        loop_count = 0
        #while time.time() - start < 5:
        while loop_count < 5:
            loop_count += 1
            print("{0}: {1}".format(self._sname, time.time()))
            time.sleep(1)

        print("{} end {}".format(self._sname, time.time()))

if __name__ == "__main__":
    # how to excute unittest via doctest
    # python -m doctest filename.py -v
    import doctest
    doctest.testmod()