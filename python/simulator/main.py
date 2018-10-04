#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading

import crc
import memorymapping

class Inverter(object):
    def __init__(self, id):
        self.lock = threading.RLock()
        self.id = id
        self.alarm = 0x00000000
        self.error = 0x00000000
        self.reflash_timestamp = time.time()
        self.TotalOutputPower = 0
        self.mm = memorymapping.MemoryMapping(0xc000, 0xc020)
        for i, val in enumerate(self.mm.memory):
            self.mm.memory[i] = i

    def __str__(self):
        return 'Inverter-{}, {} KW, {} KWH'.format(
            self.id, 
            round(self.OutputPower/1000,3), 
            round(self.TotalOutputPower/1000,3))

    def reflash(self):
        diff = time.time() - self.reflash_timestamp
        self.OutputPower = (5000/3600)*diff
        self.TotalOutputPower += self.OutputPower

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
                print('ID error')
                return None

            # crc check
            if not crc.check_crc16(querypacket):
                print('CRC error')
                return None

            # address check
            if not address >= self.mm.start_address:
                print('address error')
                return None
            if not ((address+wordlength) <= self.mm.end_address):
                print('address error')
                return None

            # prepare response
            resphex = '{:02x} {:02x} {:02x}'.format(
                slavenumber, 
                functioncode, 
                wordlength*2)
            resp = bytearray.fromhex(resphex)
            startindex = (address - self.mm.start_address) * 2
            endindex = startindex + (wordlength*2) 
            data = self.mm.dump_from(address, wordlength)
            d = ' '.join(['{:04x}'.format(b) for b in data])
            data = bytearray.fromhex(d)

            resp = resp + data
            resp = crc.append_crc16(resp)
            return resp


def main():
    inv = Inverter(1)

    '''for _ in range(1, 10):
        inv.reflash()
        print(inv)
        time.sleep(1)
        '''


    q = '01 03 c0 00 00 02'
    q = bytearray.fromhex(q)
    q = crc.append_crc16(q)
    print('query: {}'.format(q))

    r = inv.read_memory_by_jbus(q)
    print('return: {}'.format(r))





if __name__ == '__main__':

    main()
