#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import crc


class Jbus(object):
    def __init__(self, ser):
        self.ser = ser
        self.txpacket = None
        self.rxpacket = None

    #def invoke(self, txpacket, expectlen=None):
    def action(self, txpacket, expectlen=None):
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        self.ser.write(txpacket)
        self.ser.flush()
        time.sleep(0.2) # wait for machine processing 
        if expectlen:
            result = self.ser.read(expectlen)
        else:
            time.sleep(1) # force wait
            result = self.ser.read(self.ser.in_waiting)
        return result

    def isvalid(self, txpacket, rxpacket):
        if not rxpacket :                       raise ValueError('no response')
        if not crc.check_crc16(rxpacket):       raise ValueError('crc error')
        if not (rxpacket[0] == txpacket[0]):    raise ValueError('id error')
        if not (rxpacket[1] == txpacket[1]):    raise ValueError('function error')
        return True


    def read(self, id, addr, wordlen):
        hexstr = '{id:02x} 03 {addrh:02x} {addrl:02x} {wordlenh:02x} {wordlenl:02x}'.format(
            id = id,
            addrh = addr >> 8 & 0xff,
            addrl = addr & 0xff,
            wordlenh = wordlen >> 8 & 0xff,
            wordlenl = wordlen & 0xff)
        ba = bytearray.fromhex(hexstr)
        self.txpacket = crc.append_crc16(ba)
        expectlen = 3 + wordlen*2 + 2
        self.rxpacket = ''
        #self.rxpacket = self.invoke(self.txpacket, expectlen)
        self.rxpacket = self.action(self.txpacket, expectlen)
        if self.isvalid(self.txpacket, self.rxpacket):
            return self.rxpacket


    def write(self, id, addr, payload):
        payloadbytes = payload.split(' ')
        bytelen = len(payloadbytes)
        wordlen = bytelen // 2
        hexstr = '{id:02x} 10 {addrh:02x} {addrl:02x} {wordlenh:02x} {wordlenl:02x} {bytelen:02x} {payload}'.format(
            id=id,
            addrh = addr >> 8 & 0xff,
            addrl = addr & 0xff,
            wordlenh = wordlen >> 8 & 0xff,
            wordlenl = wordlen & 0xff,
            bytelen = bytelen,
            payload = payload)
        ba = bytearray.fromhex(hexstr)
        self.txpacket = crc.append_crc16(ba)
        expectlen = 8
        self.rxpacket = ''
        #self.rxpacket = self.invoke(self.txpacket, expectlen)
        self.rxpacket = self.action(self.txpacket, expectlen)
        if self.isvalid(self.txpacket, self.rxpacket):
            return self.rxpacket


    def read_with_retry(self, id, addr, wordlen, retry=3):
        i = 0
        while i < retry:
            try:
                return self.read(id, addr, wordlen)
            except ValueError as ex: 
                #print(repr(ex))
                pass
            i += 1
        raise ValueError('retry fail')


    def write_with_retry(self, id, addr, payload, retry=3):
        i = 0
        while i < retry:
            try:
                return self.write(id, addr, payload)
            except ValueError as ex: 
                #print(repr(ex))
                pass
            i += 1
        raise ValueError('retry fail')




def intergration_test():
    import serial
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.8)

    j = Jbus(ser)
    start = time.time()
    try:
        #result = j.read_with_retry(1, 0xc081, 64, retry=3)
        result = j.read_with_retry(1, 0xc000, 10)
        print(' '.join(['{:02x}'.format(b) for b in result]))
        print('spend: {}'.format(time.time()-start))
    except ValueError as ex:
        pass

    '''
    start = time.time()
    result = j.write(1, 0xc082, 'AA BB')
    print(' '.join(['{:02x}'.format(b) for b in result]))
    print('spend: {}'.format(time.time()-start))
    '''


if __name__ == '__main__':
    intergration_test()
