#!/usr/bin/env python3
import threading
import time
import queue
import sys

import recorderdb
import event
import pvinverter

class Collector(threading.Thread):
    def __init__(self, obus):
        threading.Thread.__init__(self)       
        self.obus = obus


    def run(self):
    
        pvgroup = [pvinverter.PVInverter(i) for i in range(1,3)]
        [print(pv) for pv in pvgroup]


        ltime = time.localtime()
        while True:

            [pv.sync_with_hardware() for pv in pvgroup]
            #[print(pv) for pv in pvgroup]


            # event
            for pv in pvgroup:
                for e in pv.events:
                    e.onlinecount = 2
                    self.obus.event.put(e)
                pv.events.clear()


            if time.localtime().tm_min != ltime.tm_min:
                print('New minute: {}'.format(ltime.tm_min))
                for pv in pvgroup:
                    r = pv.make_record()
                    print('Generate new measurement: {}'.format(r))
                    self.obus.measure.put(r)


                ltime = time.localtime()

            time.sleep(1)
