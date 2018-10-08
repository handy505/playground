#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime

import crc
import memorymapping
import concatenate


class JbusDevice(object):
    def __init__(self, id):
        self.lock = threading.RLock()
        self.id = id

    def read_memory_by_jbus(self, querypacket):
        with self.lock:
            if len(querypacket) < 6:
                return None

            slavenumber = querypacket[0]
            functioncode = querypacket[1]
            address = (querypacket[2] << 8) + querypacket[3]
            wordlength = querypacket[5]

            # id check
            if slavenumber != self.id:
                #print('ID error')
                return None
            # crc check
            if not crc.check_crc16(querypacket):
                #print('CRC error')
                return None
            if functioncode != 3:
                print('Not support function code {}'.format(functioncode))
                return None
            # address check
            if not address >= self.mm.start_address:
                #print('address error')
                return None
            if not ((address+wordlength) <= self.mm.end_address):
                #print('address error')
                return None

            # prepare response
            resphex = '{:02x} {:02x} {:02x}'.format(
                slavenumber, 
                functioncode, 
                wordlength*2)
            resp = bytearray.fromhex(resphex)
            startindex = (address - self.mm.start_address) * 2
            endindex = startindex + (wordlength*2) 
            data = self.mm.dump(address, wordlength)
            d = ' '.join(['{:04x}'.format(b) for b in data])
            data = bytearray.fromhex(d)

            resp = resp + data
            resp = crc.append_crc16(resp)
            return resp


class DCBoxIlluMeter(JbusDevice):
    def __init__(self, id):
        super().__init__(id)
        self.mm = memorymapping.MemoryMapping(0x0000, 0x0027)
        value = 0 
        self.mm.write(0x0003, value) # DP

    def refresh(self):
        with self.lock:
            value = random.randint(4, 8)
            self.mm.write(0x0019, value) # DISPLAY


class DCBoxTempMeter(JbusDevice):
    def __init__(self, id):
        super().__init__(id)
        self.mm = memorymapping.MemoryMapping(0x0000, 0x0027)
        value = 1
        self.mm.write(0x0003, value) # DP

    def refresh(self):
        with self.lock:
            value = random.randint(8500, 8502)
            self.mm.write(0x0019, value) # DISPLAY



class Inverter(JbusDevice):
    def __init__(self, id):
        super().__init__(id)
        self.mm = memorymapping.MemoryMapping(0xc000, 0xc060)

    def __str__(self):
        kw = self.mm.read(0xc020)
        highbyte = self.mm.read(0xc031)
        lowbyte  = self.mm.read(0xc032)
        kwh = (highbyte << 8) | lowbyte 
        return 'Inverter-{}, {} KW, {} KWH'.format(
            self.id, 
            round(kw/1000,3), 
            round(kwh/1000,3))

    def refresh(self):
        with self.lock:

            '''value = random.randint(100,200)
            self.mm.write(0xc010, value)

            value = random.randint(200,300)
            self.mm.write(0xc011, value)
            '''

            kw = random.randint(0,10)
            self.mm.write(0xc020, kw)

            word0 = self.mm.read(0xc031)
            word1 = self.mm.read(0xc032)
            kwh = (word0 << 16) | word1
            kwh += kw 
            word1 = (kwh >> 16) & 0xffff
            word0 = kwh & 0xffff
            self.mm.write(0xc031, word1)
            self.mm.write(0xc032, word0)



class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.invgroup = []
        for id in range(1, 3):
            inv = Inverter(id)
            print(inv)
            self.invgroup.append(inv)

        self.imeter = DCBoxIlluMeter(11)
        self.tmeter = DCBoxTempMeter(10)
            
        self.concatthread = concatenate.ConcatThread(self.invgroup, self.imeter, self.tmeter)

    def run(self):

        refresh_timestamp = time.time()

        self.concatthread.start()
        while True:
            now = time.time()
            if now - refresh_timestamp > 3:
                for inv in self.invgroup:
                    inv.refresh()

                self.imeter.refresh()
                self.tmeter.refresh()

                #dt = datetime.datetime.fromtimestamp(now)
                #print('Refresh at {}'.format(dt))
                refresh_timestamp = now


def main():
    print('PV Inverter simulator')
    mainthread = MainThread()
    mainthread.start()


def demo():

    inv = Inverter(1)
    imeter = DCBoxIlluMeter(10)
    tmeter = DCBoxTempMeter(11)

    group = [inv, imeter, tmeter]


    #q = '01 03 c0 31 00 02'
    q = '0a 03 00 19 00 01'
    q = bytearray.fromhex(q)
    q = crc.append_crc16(q)
    #print('query: {}'.format(q))

    [dev.refresh() for dev in group]

    for dev in group:
        r = dev.read_memory_by_jbus(q)
        if r:
            s = ' '.join(['{:02x}'.format(b) for b in r])
            print('return: {}'.format(s))


if __name__ == '__main__':

    main()
