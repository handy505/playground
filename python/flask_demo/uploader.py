#!/usr/bin/env python3
import time
import threading
import sqlite3
from datetime import datetime


class UploaderThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.dbproxy = DBProxy()
        self.uid = 0


    def run(self):
        while True:
            rows = self.dbproxy.read_from_uid(self.uid)

            print('---------------------')
            [print(row) for row in rows]
            self.uid = rows[-1][0]

            self.dbproxy.update_uploaded_by_uid(self, uid):

            time.sleep(1)


if __name__ == '__main__':
    ut = UploaderThread()
    ut.start()
