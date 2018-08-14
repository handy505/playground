#!/usr/bin/env python3
import threading
import time
import queue
import sys

import collector
import recorderdb
import uploader
import hearbeat


class Bus(object):
    def __init__(self):
        self.event = queue.Queue()
        self.measure = queue.Queue()
        self.measurehour = queue.Queue()
        self.illu = queue.Queue()
        self.illuhour = queue.Queue()
        self.temp = queue.Queue()
        self.temphour = queue.Queue()

def main():

    abus = Bus()
    bbus = Bus()
    cbus = Bus()

    ct = collector.Collector(abus)
    rt = recorderdb.RecorderDB(abus, bbus, cbus)
    ut = uploader.Uploader(bbus, cbus)
    ht = hearbeat.Hearbeat()

    ct.start()
    rt.start()
    ut.start()
    ht.start()

    ct.join()
    rt.join()
    ut.join()
    ht.join()


if __name__ == '__main__':
    main()


