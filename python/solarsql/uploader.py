#!/usr/bin/env python3
import threading
import time
import queue
import sys

import recorderdb
import event


class Uploader(threading.Thread):
    def __init__(self, ibus, obus):
        threading.Thread.__init__(self)       
        self.ibus = ibus 
        self.obus = obus 

    def run(self):
        while True:
            self.event_uploading()
            time.sleep(1)


    def event_uploading(self):
        rows = []
        while not self.ibus.event.empty():
            row = self.ibus.event.get()
            rows.append(row)

        uids = [row.uid for row in rows]
        [self.obus.event.put(uid) for uid in uids]
