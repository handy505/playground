#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading


class UploadTask(threading.Thread):
    """
    上傳，從檔案拿紀錄打包成JSON上傳
    1) 每分鐘
    2) 每小時
    3) 維護與server的長連接
    4) 更新設定檔，維護xuidu(已上傳id: muidu, huidu)
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self._name = "upload_task"
        self._sname = "[u]"

    def run(self):
        start = time.time()
        print("{} start at {}".format(self._sname, start))

        loop_count = 0
        while loop_count < 5:
            loop_count += 1
            print("{0}: {1}".format(self._sname, time.time()))
            time.sleep(3)

        print("{} end {}".format(self._sname, time.time()))

if __name__ == "__main__":
    # python3 -m doctest filename.py -v
    import doctest
    doctest.testmod()