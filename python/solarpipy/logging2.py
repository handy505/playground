#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading

"""
檔名不要取成 logging.py
常用字會導致doctest發生錯誤
"""
class LoggingTask(threading.Thread):
    """
    紀錄，從pv inverter拿資料寫入檔案
    1) 每分鐘
    2) 每小時
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self._name = "logging_task"
        self._sname = "[l]"

    def run(self):
        start = time.time()
        print("{} start at {}".format(self._sname, start))

        loop_count = 0
        #while time.time() - start < 5:
        while loop_count < 5:
            loop_count += 1
            print("{0}: {1}".format(self._sname, time.time()))
            time.sleep(2)

        print("{} end {}".format(self._sname, time.time()))

if __name__ == "__main__":
    # python3 -m doctest filename.py -v
    import doctest
    doctest.testmod()