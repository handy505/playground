#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import random
import time

import crc
import memorymapping

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


class PDUBoard(JbusDevice):
    def __init__(self, id):
        super().__init__(id)
        self.mm = memorymapping.MemoryMapping(0x0000, 0xffff)
        self.start_timestamp = time.time()

    def __str__(self):
        value = self.mm.read(0x0240)
        return 'PDUBoard-{},value:{}'.format(self.id, value) 

    def refresh(self):
        with self.lock:
            value = time.time() - self.start_timestamp
            self.mm.write(0x0240, int(value))


if __name__ == '__main__':
    board = PDUBoard(1)

    while True:
        board.refresh()
        print(board)
        time.sleep(1)

