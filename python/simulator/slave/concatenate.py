#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import serial


class ConcatThread(threading.Thread):
    def __init__(self, pvgroup=None, imeter=None, tmeter=None):
        threading.Thread.__init__(self)       
        self.pvgroup = pvgroup
        self.imeter = imeter
        self.tmeter = tmeter
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
        #self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)
        self.looping = True


    def run(self):
        rxlen = 0
        mode = 'idle'
        checktime = time.time() 
        while self.looping:
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
                self.processing(rxpacket)
                mode = 'idle'
                rxlen = 0
            time.sleep(0.01)


    def processing(self, rxpacket):
        s = ' '.join(['{:02x}'.format(b) for b in rxpacket]) # debug
        print('{:.3f}: {}'.format(time.time(), s))

        #for i, pv in enumerate(self.pvgroup.pool):
        for i, pv in enumerate(self.pvgroup):
            try:
                #txpacket = pv.response_jbus_query_packet(rxpacket)
                txpacket = pv.read_memory_by_jbus(rxpacket)
                if txpacket:
                    self.ser.write(txpacket)
                    self.ser.flush()
                    return
            except ValueError as ex: 
                pass

        #txpacket = self.imeter.response_jbus_query(rxpacket)
        txpacket = self.imeter.read_memory_by_jbus(rxpacket)
        if txpacket:
            self.ser.write(txpacket)
            self.ser.flush()
            return

        #txpacket = self.tmeter.response_jbus_query(rxpacket)
        txpacket = self.tmeter.read_memory_by_jbus(rxpacket)
        if txpacket:
            self.ser.write(txpacket)
            self.ser.flush()
            return
