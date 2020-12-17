#!/usr/bin/env python3
import time
import random
import threading
from datetime import datetime

from inverter import Inverter, Record
from collector import CollectorThread



class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.inverters = self.create_inverters()
        [print(inv) for inv in self.inverters]

        self.cthread = CollectorThread(self.inverters)


    def run(self):
        self.cthread.start()

        while True:
            #print('mainthread: system maintain')
            time.sleep(3)


    def now(self):
        return datetime.now()


    def create_inverters(self):
        result = [] 
        for id in range(1, 20):
            inv = Inverter(id)
            result.append(inv)
        return result


if __name__ == '__main__':
    mainthread = MainThread()
    mainthread.start()

