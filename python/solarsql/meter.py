#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
import serial
import serial.tools.list_ports
import collections
import sys
import os
import re
import queue
import statistics
import threading
import random


class MeterRecord(object):
    def __init__(self, deviceid, logtime, value):
        self.uid = 88
        self.mid = deviceid
        self.timestamp = logtime
        self.value = value

    def __str__(self):
        ts=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp))
        return '{},{},{}'.format(self.mid, ts, self.value)

class MeterRecord_bkp(object):
    def __init__(self, deviceid, logtime, value):
        self.uniqueid = 88
        self.deviceid = deviceid
        self.logtime = logtime
        self.value = value

    def __str__(self):
        ts=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.logtime))
        return '{},{},{}'.format(self.deviceid, ts, self.value)


class Meter(object):
    def __init__(self, id, port, brand, type):
        self.id = id 
        self.port = port
        self.buffer = queue.deque()
        self.brand = brand
        self.type = type

        self.lock = threading.RLock()
        self._comm_count = 0
        self._comm_success_count = 0
        self._reset_counts = False

    @property
    def reset_counts(self):
        with self.lock:
            return self._reset_counts

    @reset_counts.setter
    def reset_counts(self, arg):
        with self.lock:
            self._reset_counts = arg

    @property
    def comm_count(self):
        with self.lock:
            return self._comm_count

    @comm_count.setter
    def comm_count(self, arg):
        with self.lock:
            self._comm_count = arg

    @property
    def comm_success_count(self):
        with self.lock:
            return self._comm_success_count

    @comm_success_count.setter
    def comm_success_count(self, arg):
        with self.lock:
            self._comm_success_count = arg


    def read(self, push_buffer=True):
        pass

    def read_average(self):
        try:
            mean = int(statistics.mean(self.buffer))
            return MeterRecord(self.id, time.time(), mean)
        except statistics.StatisticsError as ex:
            print(repr(ex))
            
    def __str__(self):
        #return '{}, {}-{}'.format(self.brand, self.type, self.id)
        return '{} {}-{}'.format(self.brand, self.type, self.id)



class DCBoxMeter(Meter):

    def read(self):
        value = round(random.random()*100, 1)
        return MeterRecord(self.id, time.time(), value)

    def read_bkp(self, push_buffer=True):
        ''' Johnson's little wish:
            - meter will always polling as like inverter. not only once on every minute.
            - parameter push_buffer is designed for Johnson's little wish.
        '''
        try:
            if self.reset_counts:
                self.comm_count = 0
                self.comm_success_count = 0
                self.reset_counts = False

            self.comm_count += 1

            jb = jbus.Jbus(self.port)
            result = jb.read(self.id, 0x03, 23)

            # debug
            debug = ' '.join(['{:02x}'.format(b) for b in result])
            #print('rx: {}'.format(debug))

            #value = int.from_bytes(result[-4:-2], byteorder='big')
            value = int.from_bytes(result[-4:-2], byteorder='big', signed=True)
            #print('raw value: {}'.format(value))

            decimal_point = int.from_bytes(result[3:5], byteorder='big')
            #print('dp: {}'.format(decimal_point))
            
            if decimal_point == 0:      value = int(value/1)
            elif decimal_point == 1:    value = int(value/10)
            elif decimal_point == 2:    value = int(value/100)
            elif decimal_point == 3:    value = int(value/1000)
            #print('value: {}'.format(value))

            if value and push_buffer:
                self.buffer.append(value)
                if len(self.buffer) > 60:   
                    self.buffer.popleft()

            self.comm_success_count += 1
            return MeterRecord(self.id, time.time(), value)

        except ValueError as ex:
            print('Exception in {} read(), {}'.format(str(self), repr(ex)))
        except (serial.SerialException, Exception) as ex:
            print('Exception in {} read(), {}'.format(str(self), repr(ex)))


class JDAMeter(Meter):
    def read(self, push_buffer=True):
        ''' Johnson's little wish:
            - meter will always polling as like inverter. not only once on every minute.
            - parameter push_buffer is designed for Johnson's little wish.
        '''
        try:
            if self.reset_counts:
                self.comm_count = 0
                self.comm_success_count = 0
                self.reset_counts = False

            self.comm_count += 1

            jb = jbus.Jbus(self.port)
            result = jb.read(self.id, 0x07, 2)

            # debug
            debug = ' '.join(['{:02x}'.format(b) for b in result])
            print('rx: {}'.format(debug))

            value = int.from_bytes(result[3:5], byteorder='big')
            print('raw value: {}'.format(value))

            decimal_point = int.from_bytes(result[5:7], byteorder='big')
            print('dp: {}'.format(decimal_point))
            
            if decimal_point == 0:      value = int(value/1)
            elif decimal_point == 1:    value = int(value/10)
            elif decimal_point == 2:    value = int(value/100)
            elif decimal_point == 3:    value = int(value/1000)
            print('value: {}'.format(value))

            if value and push_buffer:
                self.buffer.append(value)
                if len(self.buffer) > 60:   
                    self.buffer.popleft()

            self.comm_success_count += 1
            return MeterRecord(self.id, time.time(), value)

        except ValueError as ex:
            print('Exception in {} read(), {}'.format(str(self), repr(ex)))
        except (serial.SerialException, Exception) as ex:
            print('Exception in {} read(), {}'.format(str(self), repr(ex)))


class CTEMeter(Meter):
    def read(self, push_buffer=True):
        ''' Johnson's little wish:
            - meter will always polling as like inverter. not only once on every minute.
            - parameter push_buffer is designed for Johnson's little wish.
        '''
        try:
            if self.reset_counts:
                self.comm_count = 0
                self.comm_success_count = 0
                self.reset_counts = False

            self.comm_count += 1

            jb = jbus.Jbus(self.port)
            result = jb.read(self.id, 0x07, 2)

            # debug
            debug = ' '.join(['{:02x}'.format(b) for b in result])
            print('rx: {}'.format(debug))


            value = int.from_bytes(result[3:5], byteorder='big')
            print('raw value: {}'.format(value))

            decimal_point = int.from_bytes(result[5:7], byteorder='big')
            print('dp: {}'.format(decimal_point))
            
            if decimal_point == 0:      value = int(value/1)
            elif decimal_point == 1:    value = int(value/10)
            elif decimal_point == 2:    value = int(value/100)
            elif decimal_point == 3:    value = int(value/1000)
            print('value: {}'.format(value))

            if value and push_buffer:
                self.buffer.append(value)
                if len(self.buffer) > 60:   
                    self.buffer.popleft()

            self.comm_success_count += 1
            return MeterRecord(self.id, time.time(), value)

        except ValueError as ex:
            print('Exception in {} read(), {}'.format(str(self), repr(ex)))
        except (serial.SerialException, Exception) as ex:
            print('Unexpect exception in {} read(), {}'.format(str(self), repr(ex)))



jda_illu_meters = (
    'illu-JDA-MD/PW', 
    'illu-JDA-W')
cte_illu_meters = (
    'illu-CTEC04-E1-1-A1')
dcbox_illu_meters = (
    'illu-MA4-DVO-A-Y', 
    'illu-MA5-DVO-A-Y', 
    'illu-MA5H-A-2A6-A-NNY',
    'illu-dcbox')


def illumination_meter_factory(conf_string, serialports):
    try:
        lines = conf_string.split('\n')
        for line in lines:
            line = line.strip(' \n')
            fields = line.split('=')
            param = fields[0]

            if param in jda_illu_meters:
                values = fields[1].split(',')
                if len(values) == 2:
                    meterid = values[0]
                    meterportnum = values[1]
                    ser = serialports[0] if meterportnum == '0' else serialports[1]
                    return JDAMeter(id=int(meterid), port=ser, brand='JDA', type='illu')
                else:
                    print('Illu meter have NOT configurated')
                    return None

            elif param in cte_illu_meters:
                values = fields[1].split(',')
                if len(values) == 2:
                    meterid = values[0]
                    meterportnum = values[1]
                    ser = serialports[0] if meterportnum == '0' else serialports[1]
                    return CTEMeter(id=int(meterid), port=ser, brand='CTE', type='illu')
                else:
                    print('Illu meter have NOT configurated')
                    return None

            elif param in dcbox_illu_meters:
                values = fields[1].split(',')
                if len(values) == 2:
                    meterid = values[0]
                    meterportnum = values[1]
                    ser = serialports[0] if meterportnum == '0' else serialports[1]
                    return DCBoxMeter(id=int(meterid), port=ser, brand='DCBox', type='illu')
                else:
                    print('Illu meter have NOT configurated')
                    return None

    except Exception as ex:
        print(repr(ex))
        return None


jda_temp_meters = (
    'temp-JDA-TD4/TD', 
    'temp-JDA-T')
cte_temp_meters = (
    'temp-CTEC04-C-B4-1-A')
dcbox_temp_meters = (
    'temp-MA4-TTO-A-Y', 
    'temp-MA5-TTO-A-Y', 
    'temp-MA5H-A-TTO-A-NNY',
    'temp-dcbox')

def temperature_meter_factory(conf_string, serialports):
    try:
        lines = conf_string.split('\n')
        for line in lines:
            line = line.strip(' \n')
            fields = line.split('=')
            param = fields[0]

            if param in jda_temp_meters:
                values = fields[1].split(',')
                if len(values) == 2:
                    meterid = values[0]
                    meterportnum = values[1]
                    ser = serialports[0] if meterportnum == '0' else serialports[1]
                    return JDAMeter(id=int(meterid), port=ser, brand='JDA', type='temp')

                else:
                    print('Temp meter have NOT configurated')
                    return None

            elif param in cte_temp_meters:
                values = fields[1].split(',')
                if len(values) == 2:
                    meterid = values[0]
                    meterportnum = values[1]
                    ser = serialports[0] if meterportnum == '0' else serialports[1]
                    return CTEMeter(id=int(meterid), port=ser, brand='CTE', type='temp')
                else:
                    print('Temp meter have NOT configurated')
                    return None

            elif param in dcbox_temp_meters:
                values = fields[1].split(',')
                if len(values) == 2:
                    meterid = values[0]
                    meterportnum = values[1]
                    ser = serialports[0] if meterportnum == '0' else serialports[1]
                    return DCBoxMeter(id=int(meterid), port=ser, brand='DCBox', type='temp')
                else:
                    print('Temp meter have NOT configurated')
                    return None
    except Exception as ex:
        print(repr(ex))
        return None


def main():

    '''#configs = 'illu-dcbox=1,0\ntemp-dcbox=2,0'
    #configs = 'illu-dcbox=3,0\ntemp-dcbox=4,0'
    configs = 'illu-dcbox=2,0\ntemp-dcbox=1,0'
    #configs = 'illu-MA4-DVO-A-Y=1,0\ntemp-MA4-TTO-A_Y=2,0'
    #configs = 'illu-JDA-MD/PW=5,0\ntemp-JDA-TD4/TD=2,0'

    # illumination / temperature meter
    imeter = illumination_meter_factory(configs)
    tmeter = temperature_meter_factory(configs)

    print(imeter)
    print(tmeter)

    value = imeter.read()
    print(value)
    value = tmeter.read()
    print(value)
    '''

    try:
        ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.8)
    except OSError as ex:
        print('Exception in generate meter with ser: {}'.format(repr(ex)))
        sys.exit()

    meters = []
    m = DCBoxMeter(id=1, port=ser, brand='DCBox', type='illu')
    meters.append(m)

    m = DCBoxMeter(id=2, port=ser, brand='DCBox', type='temp')
    meters.append(m)

    m = DCBoxMeter(id=3, port=ser, brand='DCBox', type='illu')
    meters.append(m)

    m = DCBoxMeter(id=4, port=ser, brand='DCBox', type='temp')
    meters.append(m)

    m = DCBoxMeter(id=5, port=ser, brand='DCBox', type='temp')
    meters.append(m)

    m = DCBoxMeter(id=6, port=ser, brand='DCBox', type='illu')
    meters.append(m)


    while True:
        for m in meters:
            print(m)
            print(m.read())
            time.sleep(1)




if __name__ == '__main__':

    m = DCBoxMeter(mid=1, port=None, brand='DCBox', type='illu')

    print(m.read())
    print(m.read())
    print(m.read())
    print(m.read())
