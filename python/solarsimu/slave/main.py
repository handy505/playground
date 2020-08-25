#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime

import crc
import memorymapping
import concatenate
import devices

def dumphex(pkt):
    result = ' '.join(['{:02x}'.format(b) for b in pkt]) # debug
    return result


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.inverters = []
        for id in range(1, 3):
            inv = devices.Inverter(id)
            print(inv)
            self.inverters.append(inv)

        self.imeter = devices.DCBoxIlluMeter(11)
        self.tmeter = devices.DCBoxTempMeter(10)

        '''self.modbuslistener = concatenate.ModbusListener(self.inverters, 
                                                         self.imeter, 
                                                         self.tmeter)
                                                         '''

        self.modbuslistener = concatenate.ModbusListener(callback=self.response_modbus_packet)




    def run(self):
        refresh_timestamp = time.time()
        self.modbuslistener.start()
        while True:
            now = time.time()
            if now - refresh_timestamp > 3:

                #[inv.refresh() for inv in self.inverters]
                #self.imeter.refresh()
                #self.tmeter.refresh()

                refresh_timestamp = now


    def response_modbus_packet(self, rxpacket):
        print('{:.3f}: {}'.format(time.time(), dumphex(rxpacket)))
        #print('[35;42m{:.3f}:[m {}'.format(time.time(), dumphex(rxpacket)))

        
        #print('[31m{:.3f}:[m {}'.format(time.time(), dumphex(rxpacket)))

        '''import random
        c = random.randint(31, 37)
        print('[{}m{:.3f}:[m {}'.format(c, time.time(), dumphex(rxpacket)))
        '''

        for i, pv in enumerate(self.inverters):
            try:
                result = pv.read_memory_by_jbus(rxpacket)
                return result
            except ValueError as ex: 
                pass

        result = self.imeter.read_memory_by_jbus(rxpacket)
        return result

        result = self.tmeter.read_memory_by_jbus(rxpacket)
        return result 


def main():
    print('PV Inverter simulator')
    mainthread = MainThread()
    mainthread.start()


if __name__ == '__main__':

    main()
