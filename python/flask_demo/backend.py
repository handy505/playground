#!/usr/bin/env python3
import time
import random
import threading
from datetime import datetime

from inverter import Inverter, Record
from collector import CollectorThread



class MainThread(threading.Thread):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        super().__init__()

        self.inverters = [Inverter(id) for id in range(1, 3)]
        [print(inv) for inv in self.inverters]
        
        self.cthread = CollectorThread(self.inverters)
        

        print('*** Backend main thread initialize DONE')


    def run(self):
        self.cthread.start()

        while True:
            time.sleep(3)


if __name__ == '__main__':
    mainthread = MainThread()
    mainthread.start()

