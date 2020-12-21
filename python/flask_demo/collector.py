#!/usr/bin/env python3
import time
import threading
import sqlite3
from datetime import datetime

from dbproxy import DBProxy


class CollectorThread(threading.Thread):
    def __init__(self, inverters):
        super().__init__()
        self.inverters = inverters

        self.dbproxy = DBProxy()
        self.dbproxy.create_table()

        self.datetime_of_output_action = datetime.now()


    def run(self):
        while True:
            for inv in self.inverters:
                inv.sync_with_hardware()

            
            # every minute
            if datetime.now().minute != self.datetime_of_output_action.minute:

                rec = inv.get_record()
                self.dbproxy.insert_record(rec)
                    
                self.datetime_of_output_action = datetime.now()

            time.sleep(3)




if __name__ == '__main__':
    
    from inverter import Inverter, Record
    inverters = [Inverter(id) for id in range(1,3)]

    while True:

        for inv in inverters:
            rec = inv.get_record()
            print(rec)

        time.sleep(1)
    

