#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import serial

def dumphex(pkt):
    result = ' '.join(['{:02x}'.format(b) for b in pkt]) # debug
    return result


class ModbusListener(threading.Thread):
    def __init__(self, pvgroup=None, imeter=None, tmeter=None, callback=None, args=None):
        threading.Thread.__init__(self)       
        self.pvgroup = pvgroup
        self.imeter = imeter
        self.tmeter = tmeter
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
        self.running = True
        self.args = args

        print('callback: {}'.format(callback))
        self.callback = callback

    def run(self):
        rxlen = 0
        mode = 'idle'
        checktime = time.time() 
        while self.running:
            if mode == 'idle':
                if self.ser.in_waiting > rxlen:
                    rxlen = self.ser.in_waiting
                    checktime = time.time()
                    mode = 'busy'
            elif mode == 'busy':
                TIMEOUT_CONDITION = 0.05
                if time.time() - checktime > TIMEOUT_CONDITION:
                    mode = 'timeout'
                else:
                    if self.ser.in_waiting > rxlen:
                        rxlen = self.ser.in_waiting
                        checktime = time.time()
            elif mode == 'timeout':
                rxpacket = self.ser.read(self.ser.in_waiting)

                #self.processing(rxpacket)
                txpacket = self.callback(rxpacket, self.args)
                if txpacket:
                    #print('[32m{}[m'.format(dumphex(txpacket)))
                    self.ser.write(txpacket)
                    self.ser.flush()

                mode = 'idle'
                rxlen = 0
            time.sleep(0.01)

            
def echo(pkt):
    print('echo: {}'.format(pkt))
    return pkt

if __name__ == '__main__':

    m = ModbusListener(callback=echo)
    m.start()

