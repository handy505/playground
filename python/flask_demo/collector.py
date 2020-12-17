#!/usr/bin/env python3
import time
import threading


class CollectorThread(threading.Thread):
    def __init__(self, inverters):
        super().__init__()
        self.inverters = inverters


    def run(self):
        while True:
            for inv in self.inverters:
                rec = inv.get_record()
                #print('collectorthread: {}'.format(rec))
            time.sleep(1)

