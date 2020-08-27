#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import serial
import datetime
import collections
import statistics
import threading
from inverter_base import InverterProxy
from enum import Enum

import crc
import jbus
import observer

def create_ablerex_inverters(configurations):
    try:
        result = []
        lines = configurations.splitlines() 
        for line in lines:
            if line.startswith('pv='):
                line = line.strip()
                valuestring = line.split('=')[1]
                values = valuestring.split(',')
                values = iter(values)
                for invid, portid in zip(values, values):
                    portname = '/dev/ttyUSB{}'.format(portid)
                    ser = serial.Serial(port=portname, baudrate=9600, timeout=0.8)
                    inv = PVInverter(int(invid), serport=ser)
                    result.append(inv)
        return result 
    except (IndexError, ValueError, OSError) as ex:
        print('Exception in kaco_inverter_factory(), {}'.format(repr(ex)))
        return []



#class PVInverter(observer.Observerable):
class PVInverter(InverterProxy, observer.Observerable):
    #def __init__(self, id, port=None):
    def __init__(self, id, serport):
        observer.Observerable.__init__(self)
        self.lock = threading.RLock()
        self.id = id
        self.type = "pv"
        self.ser = serport
        self.last_update_timestamp = self.time()

        self._online = False
        self.online_fifo = collections.deque(maxlen=8)
        self.online_event_occur = False 
        self.offline_event_occur = False 

        self.tm_jbus_write_timestamp = 0
        self.start_timestamp = self.time()

        self.last_alarm = 0x00
        self.last_error = 0x00
        self.alarm_fifo = collections.deque(maxlen=16)
        self.error_fifo = collections.deque(maxlen=16)


        self.alarm_event_handler = EventHandler(self.id, AblerexCloudEventTypeCode.ALARM.value)
        self.error_event_handler = EventHandler(self.id, AblerexCloudEventTypeCode.ERROR.value)


        self.txpacket = ''
        self.rxpacket = ''

        self._success_comm_counts = 0 
        self._total_comm_counts = 0
        self._reset_counts = False

        self._OutputPower_fifo      = collections.deque(maxlen=60)
        self._ACVolPhaseA_fifo      = collections.deque(maxlen=60)
        self._ACVolPhaseB_fifo      = collections.deque(maxlen=60)
        self._ACVolPhaseC_fifo      = collections.deque(maxlen=60)
        self._ACFrequency_fifo      = collections.deque(maxlen=60)
        self._ACOutputCurrentA_fifo = collections.deque(maxlen=60)
        self._ACOutputCurrentB_fifo = collections.deque(maxlen=60)
        self._ACOutputCurrentC_fifo = collections.deque(maxlen=60)
        self._DC1InputVol_fifo      = collections.deque(maxlen=60)
        self._DC2InputVol_fifo      = collections.deque(maxlen=60)
        self._DC1InputCurrent_fifo  = collections.deque(maxlen=60)
        self._DC2InputCurrent_fifo  = collections.deque(maxlen=60)
        self._DCBusPositiveVol_fifo = collections.deque(maxlen=60)
        self._DCBusNegativeVol_fifo = collections.deque(maxlen=60)
        self._InternalTemper_fifo   = collections.deque(maxlen=60)
        self._HeatSinkTemper_fifo   = collections.deque(maxlen=60)
        self._InputPowerA_fifo      = collections.deque(maxlen=60)
        self._InputPowerB_fifo      = collections.deque(maxlen=60)
        self._TotalOutputPower_fifo = collections.deque(maxlen=60)
        
        self._DC3InputVol_fifo      = collections.deque(maxlen=60) # for 52k
        self._DC4InputVol_fifo      = collections.deque(maxlen=60) # for 52k
        self._DC3InputCurrent_fifo  = collections.deque(maxlen=60) # for 52k
        self._DC4InputCurrent_fifo  = collections.deque(maxlen=60) # for 52k
        self._InputPowerC_fifo      = collections.deque(maxlen=60) # for 52k
        self._InputPowerD_fifo      = collections.deque(maxlen=60) # for 52k
        
        self.MIN_LOGIC_ADDRESS = 0xc000
        self.MAX_LOGIC_ADDRESS = 0xc07f
        wordlength = (0xc07f - 0xc000 + 1) * 2
        self.memorymap = bytearray(wordlength)

        self.observers = []
        self.jbus = jbus.Jbus(self.ser)
        #self.load_tmp('./data/tmp.txt')
        '''welcome_msg = '{} initial: 0x{:08x},0x{:08x},{},{}'.format( self.name, 
                                                                    self.alarm, 
                                                                    self.error, 
                                                                    self.online, 
                                                                    self.TotalOutputPower)
                                                                    '''

    def time(self):
        return time.time() # for unittest

    @property
    def reset_counts(self):
        with self.lock:
            return self._reset_counts

    @reset_counts.setter
    def reset_counts(self, arg):
        with self.lock:
            self._reset_counts = arg

    @property
    def total_comm_counts(self):
        with self.lock:
            return self._total_comm_counts

    @total_comm_counts.setter
    def total_comm_counts(self, arg):
        with self.lock:
            self._total_comm_counts = arg

    @property
    def success_comm_counts(self):
        with self.lock:
            return self._success_comm_counts

    @success_comm_counts.setter
    def success_comm_counts(self, arg):
        with self.lock:
            self._success_comm_counts = arg

    @property
    def online(self):
        with self.lock:
            return self._online
        
    @online.setter
    def online(self, arg):
        with self.lock:
            # make log when status chaned
            if arg != self._online:
                if arg == True:
                    # offline -> online
                    s = self.make_online_message()
                    self.online_fifo.append(s)
                    self.online_event_occur = True
                else:
                    # online -> offline
                    s = self.make_offline_message()
                    self.online_fifo.append(s)
                    self.offline_event_occur = True
            self._online = arg

    def make_online_message(self):
        ts=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.time()))
        #result = "{id},{ts},{type},{stat},H".format(id=self.id, ts=ts, type=0, stat='100') 
        result = "{id},{ts},{type},{bitnum},H".format(id=self.id, ts=ts, type=0, bitnum='100') 
        return result

    def make_offline_message(self):
        ts=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.time()))
        #result = "{id},{ts},{type},{stat},H".format(id=self.id, ts=ts, type=0, stat='101') 
        result = "{id},{ts},{type},{bitnum},H".format(id=self.id, ts=ts, type=0, bitnum='101') 
        return result


    @property
    def alarm(self):
        with self.lock:
            # little endian
            word0 = self._get_word_from(0xc000)
            word1 = self._get_word_from(0xc001)
            word2 = self._get_word_from(0xc002)
            word3 = self._get_word_from(0xc003)
            #return ((word1<<16) | word0)
            return ((word3<<48) | (word2<<32) | (word1<<16) | word0)

    @alarm.setter
    def alarm(self, arg):
        with self.lock:
            oldercode = self.alarm
            self._write_alarm_memory(arg)
            self.process_alarm_queue(oldercode, self.alarm)

    def _write_alarm_memory(self, arg):
        # little endian
        word0 = arg & 0xffff
        word1 = (arg>>16) & 0xffff
        self._set_word_to(0xc000, word0)
        self._set_word_to(0xc001, word1)


    def process_alarm_queue(self, older, newer):
        if self.time() - self.start_timestamp > (6*60):
            if newer != older:
                ae = AlarmEvent(self.id, older, newer, when=time.time())
                records = ae.records()
                [self.alarm_fifo.append(r) for r in records]
                

    @property
    def error(self):
        with self.lock:
            # little endian
            word0 = self._get_word_from(0xc010)
            word1 = self._get_word_from(0xc011)
            word2 = self._get_word_from(0xc012)
            word3 = self._get_word_from(0xc013)
            return ((word3<<48) | (word2<<32) | (word1<<16) | word0)

    @error.setter
    def error(self, arg):
        with self.lock:
            oldercode = self.error
            self._write_error_memory(arg)
            self.process_error_queue(oldercode, self.error)


    def _write_error_memory(self, arg):
        # little endian
        word0 = arg & 0xffff
        word1 = (arg>>16) & 0xffff
        word2 = (arg>>32) & 0xffff
        word3 = (arg>>48) & 0xffff
        self._set_word_to(0xc010, word0)
        self._set_word_to(0xc011, word1)
        self._set_word_to(0xc012, word2)
        self._set_word_to(0xc013, word3)


    def process_error_queue(self, older, newer):
        if self.time() - self.start_timestamp > (6*60):
            if newer != older:
                ee = ErrorEvent(self.id, older, newer, when=time.time())
                records = ee.records()
                [self.error_fifo.append(r) for r in records]


    def __str__(self):
        return 'AblerexInverter-{}'.format(self.id)

    @property
    def name(self):
        return "{}-{}".format(self.type, self.id)

    def create_record(self):
        return self.make_raw_record()

    #def make_raw_record(self):
    def make_raw_record(self, update_statistics=False):

        with self.lock:
            if not self.online:
                raise ValueError('{} is offline, skip make raw record'.format(self.name))

            seq = []
            seq.append(str(self.id))

            ts = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.time()))
            seq.append(ts)

            seq.append(self.OutputPower)
            seq.append(self.ACVolPhaseA)
            seq.append(self.ACVolPhaseB)
            seq.append(self.ACVolPhaseC)
            seq.append(self.ACFrequency)
            seq.append(self.ACOutputCurrentA)
            seq.append(self.ACOutputCurrentB)
            seq.append(self.ACOutputCurrentC)
            seq.append(self.DC1InputVol)
            seq.append(self.DC2InputVol)
            seq.append(self.DC1InputCurrent)
            seq.append(self.DC2InputCurrent)
            seq.append(self.DCBusPositiveVol)
            seq.append(self.DCBusNegativeVol)
            seq.append(self.InternalTemper)
            seq.append(self.HeatSinkTemper)
            seq.append(self.InputPowerA)
            seq.append(self.InputPowerB)
            seq.append(self.TotalOutputPower)
            seq.append(self.DC3InputVol) # for 52k
            seq.append(self.DC4InputVol) # for 52k
            seq.append(self.DC3InputCurrent) # for 52k
            seq.append(self.DC4InputCurrent) # for 52k
            seq.append(self.InputPowerC) # for 52k
            seq.append(self.InputPowerD) # for 52k
            result = ','.join([str(item) for item in seq])

            if update_statistics:
                self.update_statistics()

            return result 
        

    def make_hourly_record(self):
        with self.lock:
            if not self.online:
                raise ValueError('pv{} is offline, no any raw data'.format(self.id))

            seq = []
            seq.append(self.id)

            # hour record indicate LAST  hour
            ts0 = time.localtime(self.time() - (60*60)) 
            ts = '{:0=4}/{:0=2}/{:0=2} {:0=2}:00:00'.format(
                ts0.tm_year, 
                ts0.tm_mon, 
                ts0.tm_mday, 
                ts0.tm_hour)
            seq.append(ts)

            try:
                avg = statistics.mean(self._OutputPower_fifo)
                seq.append(round(avg, 2))
                avg = statistics.mean(self._ACVolPhaseA_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._ACVolPhaseB_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._ACVolPhaseC_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._ACFrequency_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._ACOutputCurrentA_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._ACOutputCurrentB_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._ACOutputCurrentC_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC1InputVol_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC2InputVol_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC1InputCurrent_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC2InputCurrent_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DCBusPositiveVol_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DCBusNegativeVol_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._InternalTemper_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._HeatSinkTemper_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._InputPowerA_fifo)
                seq.append(round(avg, 1))
                avg = statistics.mean(self._InputPowerB_fifo)
                seq.append(round(avg, 1))

                #seq.append(self.TotalOutputPower) # max value

                avg = statistics.mean(self._DC3InputVol_fifo) # for 52k
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC4InputVol_fifo) # for 52k
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC3InputCurrent_fifo) # for 52k
                seq.append(round(avg, 1))
                avg = statistics.mean(self._DC4InputCurrent_fifo) # for 52k
                seq.append(round(avg, 1))
                avg = statistics.mean(self._InputPowerC_fifo) # for 52k
                seq.append(round(avg, 1))
                avg = statistics.mean(self._InputPowerD_fifo) # for 52k
                seq.append(round(avg, 1))

                seq.append(self.TotalOutputPower) # max value


            except statistics.StatisticsError as e:
                raise ValueError('calc avg error')

            self.clear_statistics_buffers()
            result = ','.join([str(item) for item in seq]) 
            return result        

    def clear_statistics_buffers(self):
        self._OutputPower_fifo.clear()
        self._ACVolPhaseA_fifo.clear()
        self._ACVolPhaseB_fifo.clear()
        self._ACVolPhaseC_fifo.clear()
        self._ACFrequency_fifo.clear()
        self._ACOutputCurrentA_fifo.clear()
        self._ACOutputCurrentB_fifo.clear()
        self._ACOutputCurrentC_fifo.clear()
        self._DC1InputVol_fifo.clear()
        self._DC2InputVol_fifo.clear()
        self._DC1InputCurrent_fifo.clear()
        self._DC2InputCurrent_fifo.clear()
        self._DCBusPositiveVol_fifo.clear()
        self._DCBusNegativeVol_fifo.clear()
        self._InternalTemper_fifo.clear()
        self._HeatSinkTemper_fifo.clear()
        self._InputPowerA_fifo.clear()
        self._InputPowerB_fifo.clear()


    def _set_word_to(self, word_address, value):
        with self.lock:
            byte0 = value & 0xff
            byte1 = (value >> 8) & 0xff
            offset = (word_address - 0xc000) * 2
            self.memorymap[offset+1] = byte0
            self.memorymap[offset+0] = byte1


    @property
    def OutputPower(self):
        result = self._get_word_from(0xc020)
        result = round(result*0.01, 2)
        return result

    @OutputPower.setter
    def OutputPower(self, arg):
        self._set_word_to(0xc020, arg*100)


    @property
    def ACVolPhaseA(self):
        result = self._get_word_from(0xc021)
        return result

    @ACVolPhaseA.setter
    def ACVolPhaseA(self, arg):
        self._set_word_to(0xc021, arg)


    @property
    def ACVolPhaseB(self):
        result = self._get_word_from(0xc022)
        return result

    @ACVolPhaseB.setter
    def ACVolPhaseB(self, arg):
        self._set_word_to(0xc022, arg)


    @property
    def ACVolPhaseC(self):
        return self._get_word_from(0xc03e)

    @ACVolPhaseC.setter
    def ACVolPhaseC(self, arg):
        self._set_word_to(0xc03e, arg)


    @property
    def ACFrequency(self):
        result = self._get_word_from(0xc026)
        result = round(result*0.1, 1)
        return result 

    @ACFrequency.setter
    def ACFrequency(self, arg):
        self._set_word_to(0xc026, arg*10)


    @property
    def ACOutputCurrentA(self):
        result = self._get_word_from(0xc024)
        result = round(result*0.1, 1)
        return result 

    @ACOutputCurrentA.setter
    def ACOutputCurrentA(self, arg):
        self._set_word_to(0xc024, arg*10)


    @property
    def ACOutputCurrentB(self):
        result = self._get_word_from(0xc025)
        result = round(result*0.1, 1)
        return result 

    @ACOutputCurrentB.setter
    def ACOutputCurrentB(self, arg):
        self._set_word_to(0xc025, arg*10)


    @property
    def ACOutputCurrentC(self):
        result = self._get_word_from(0xc041)
        result = round(result*0.1, 1)
        return result

    @ACOutputCurrentC.setter
    def ACOutputCurrentC(self, arg):
        self._set_word_to(0xc041, arg*10)


    @property
    def DC1InputVol(self):
        return self._get_word_from(0xc02b)

    @DC1InputVol.setter
    def DC1InputVol(self, arg):
        self._set_word_to(0xc02b, arg)


    @property
    def DC2InputVol(self):
        return self._get_word_from(0xc02c)

    @DC2InputVol.setter
    def DC2InputVol(self, arg):
        self._set_word_to(0xc02c, arg)

    # for 52k
    @property
    def DC3InputVol(self):
        return self._get_word_from(0xc04e)

    @DC3InputVol.setter
    def DC3InputVol(self, arg):
        self._set_word_to(0xc04e, arg)

    # for 52k
    @property
    def DC4InputVol(self):
        return self._get_word_from(0xc04f)

    @DC4InputVol.setter
    def DC4InputVol(self, arg):
        self._set_word_to(0xc04f, arg)


    @property
    def DC1InputCurrent(self):
        result = self._get_word_from(0xc02d)
        result = round(result*0.1, 1)
        return result

    @DC1InputCurrent.setter
    def DC1InputCurrent(self, arg):
        self._set_word_to(0xc02d, arg*10)


    @property
    def DC2InputCurrent(self):
        result = self._get_word_from(0xc02e)
        result = round(result*0.1, 1)
        return result

    @DC2InputCurrent.setter
    def DC2InputCurrent(self, arg):
        self._set_word_to(0xc02e, arg*10)

    # for 52k
    @property
    def DC3InputCurrent(self):
        result = self._get_word_from(0xc050)
        result = round(result*0.1, 1)
        return result

    @DC3InputCurrent.setter
    def DC3InputCurrent(self, arg):
        self._set_word_to(0xc050, arg*10)

    # for 52k
    @property
    def DC4InputCurrent(self):
        result = self._get_word_from(0xc051)
        result = round(result*0.1, 1)
        return result

    @DC4InputCurrent.setter
    def DC4InputCurrent(self, arg):
        self._set_word_to(0xc051, arg*10)

    @property
    def DCBusPositiveVol(self):
        return self._get_word_from(0xc027)

    @DCBusPositiveVol.setter
    def DCBusPositiveVol(self, arg):
        self._set_word_to(0xc027, arg)


    @property
    def DCBusNegativeVol(self):
        return self._get_word_from(0xc028)

    @DCBusNegativeVol.setter
    def DCBusNegativeVol(self, arg):
        self._set_word_to(0xc028, arg)


    @property
    def InternalTemper(self):
        return self._get_word_from(0xc029)

    @InternalTemper.setter
    def InternalTemper(self, arg):
        self._set_word_to(0xc029, arg)


    @property
    def HeatSinkTemper(self):
        return self._get_word_from(0xc02a)

    @HeatSinkTemper.setter
    def HeatSinkTemper(self, arg):
        self._set_word_to(0xc02a, arg)


    @property
    def InputPowerA(self):
        result = self._get_word_from(0xc02f)
        result = round(result*0.01, 2)
        return result

    @InputPowerA.setter
    def InputPowerA(self, arg):
        self._set_word_to(0xc02f, arg*100)


    @property
    def InputPowerB(self):
        result = self._get_word_from(0xc030)
        result = round(result*0.01, 2)
        return result

    @InputPowerB.setter
    def InputPowerB(self, arg):
        self._set_word_to(0xc030, arg*100)

    # for 52k
    @property
    def InputPowerC(self):
        result = self._get_word_from(0xc052)
        result = round(result*0.01, 2)
        return result

    @InputPowerC.setter
    def InputPowerC(self, arg):
        self._set_word_to(0xc052, arg*100)

    # for 52k
    @property
    def InputPowerD(self):
        result = self._get_word_from(0xc053)
        result = round(result*0.01, 2)
        return result

    @InputPowerD.setter
    def InputPowerD(self, arg):
        self._set_word_to(0xc053, arg*100)

    @property
    def TotalOutputPower(self):
        # big endian, what the fuck !
        word1 = self._get_word_from(0xc031)
        word0 = self._get_word_from(0xc032)
        result = (word1<<16) | word0
        return result 

    @TotalOutputPower.setter
    def TotalOutputPower(self, arg):
        word0 = arg & 0xffff
        word1 = (arg >> 16) & 0xffff
        self._set_word_to(0xc031, word1)
        self._set_word_to(0xc032, word0)


    def write_timestamp_to_hardware(self):
        with self.lock:
            TIME_ADDR = 0xC09A # pv inverter 25.6k time address
            time_addr_high = TIME_ADDR >> 8 & 0xff
            time_addr_low = TIME_ADDR & 0xff 

            ts = time.localtime(self.time()) # get timestamp 
            year_high = ts.tm_year >> 8 & 0xff 
            year_low = ts.tm_year & 0xff 
            month = ts.tm_mon
            day = ts.tm_mday 
            hour = ts.tm_hour 
            minute = ts.tm_min 

            packet = [
                self.id, 
                0x10, 
                time_addr_high, 
                time_addr_low, 
                0x00, 
                0x03, 
                0x06, 
                year_high, 
                year_low,
                month,
                day,
                hour,
                minute]
            hexstr = ' '.join('{:02x}'.format(item) for item in packet)
            ba = bytearray.fromhex(hexstr)
            txpacket = crc.append_crc16(ba)

            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
            self.ser.write(txpacket)
            self.ser.flush()

            time.sleep(0.2)
            self.tm_jbus_write_timestamp = self.time() 


    def write_timecode_to_25k6_hardware(self):
        with self.lock:
            ts = time.localtime(self.time()) # get timestamp 
            yearh = ts.tm_year >> 8 & 0xff 
            yearl = ts.tm_year & 0xff 
            month = ts.tm_mon
            day = ts.tm_mday 
            hour = ts.tm_hour 
            minute = ts.tm_min 
            payloads = [yearh, yearl, month, day, hour, minute]
            payloadhexstr = ' '.join('{:02x}'.format(b) for b in payloads)
            try:
                self.jbus.write_with_retry(self.id, 0xc09a, payloadhexstr)
            except ValueError as ex:
                print('Exception in {} write timestamp to 25k6, {}'.format(str(self), repr(ex)))
            self.tm_jbus_write_timestamp = self.time() 
            

    def dumps(self):
        with self.lock:
            seq = []
            seq.append(str(self.id))
            fmt = '%Y/%m/%d %H:%M:%S'
            tf = time.strftime(fmt, time.localtime(self.time()))
            seq.append(tf)
            
            seq.append('{:08x}'.format(self.alarm))
            seq.append('{:08x}'.format(self.error))
            seq.append(str(self.online))

            seq.append(str(self.OutputPower))
            seq.append(str(self.ACVolPhaseA))
            seq.append(str(self.ACVolPhaseB))
            seq.append(str(self.ACVolPhaseC))
            seq.append(str(self.ACFrequency))
            seq.append(str(self.ACOutputCurrentA))
            seq.append(str(self.ACOutputCurrentB))
            seq.append(str(self.ACOutputCurrentC))
            seq.append(str(self.DC1InputVol))
            seq.append(str(self.DC2InputVol))
            seq.append(str(self.DC1InputCurrent))
            seq.append(str(self.DC2InputCurrent))
            seq.append(str(self.DCBusPositiveVol))
            seq.append(str(self.DCBusNegativeVol))
            seq.append(str(self.InternalTemper))
            seq.append(str(self.HeatSinkTemper))
            seq.append(str(self.InputPowerA))
            seq.append(str(self.InputPowerB))
            seq.append(str(self.TotalOutputPower))
            s = ",".join(seq)
            return s


    '''def load_tmp(self, filename):
        with self.lock:
            if not os.path.isfile(filename):
                return

            try:        
                with open(filename, "r", encoding="utf-8") as fr:
                    for line in fr.readlines():
                        line = line.strip("\n")
                        fields = line.split(',')
                        
                        tmpid = int(fields[0])
                        if self.id == tmpid:
                            # update value in 10mins time interval
                            struct_time = time.strptime(fields[1], '%Y/%m/%d %H:%M:%S')
                            sec = time.mktime(struct_time)
                            if self.time() - sec < (10*60):
                                code = int(fields[2], 16)
                                self._write_alarm_memory(code)
                                code = int(fields[3], 16)
                                self._write_error_memory(code)
                                #self.online = bool(fields[4])
                                self.TotalOutputPower = int(fields[-1])
                                break
            except Exception as ex:
                print('Exception in {} load_tmp(), {}'.format(str(self), repr(ex)))
                '''


    def read_memory_by_jbus(self, querypacket):
        return self.response_jbus_query_packet(querypacket)

    '''def response_jbus_query_packet(self, querypacket):
        with self.lock:
            if len(querypacket) < 6:
                return None

            slavenumber = querypacket[0]
            functioncode = querypacket[1]
            address = (querypacket[2] << 8) + querypacket[3]
            wordlength = querypacket[5]

            # id error check
            if slavenumber != self.id:
                return None

            # crc error check
            if not crc.check_crc16(querypacket):
                return None

            # address check
            if not address >= self.MIN_LOGIC_ADDRESS:
                return None
            if not ((address+wordlength) <= self.MAX_LOGIC_ADDRESS):
                return None

            # prepare response
            resphex = '{:02x} {:02x} {:02x}'.format(
                slavenumber, 
                functioncode, 
                wordlength*2)
            resp = bytearray.fromhex(resphex)
            startindex = (address - self.MIN_LOGIC_ADDRESS) * 2
            endindex = startindex + (wordlength*2) 
            data = self.memorymap[startindex:endindex]
            resp = resp + data
            resp = crc.append_crc16(resp)
            return resp
            '''

    def response_jbus_query_packet(self, querypacket):
        with self.lock:

            if not self.online: # for Tatung, when disconnect, don't response.
                return None

            if len(querypacket) < 6:
                return None

            slavenumber = querypacket[0]
            functioncode = querypacket[1]
            address = (querypacket[2] << 8) + querypacket[3]
            wordlength = querypacket[5]

            # id error check
            if slavenumber != self.id:
                return None

            # crc error check
            if not crc.check_crc16(querypacket):
                return None

            # address check
            if not address >= self.MIN_LOGIC_ADDRESS:
                return None
            if not ((address+wordlength) <= self.MAX_LOGIC_ADDRESS):
                return None

            # prepare response
            resphex = '{:02x} {:02x} {:02x}'.format(
                slavenumber, 
                functioncode, 
                wordlength*2)
            resp = bytearray.fromhex(resphex)
            startindex = (address - self.MIN_LOGIC_ADDRESS) * 2
            endindex = startindex + (wordlength*2) 
            data = self.memorymap[startindex:endindex]
            resp = resp + data
            resp = crc.append_crc16(resp)
            return resp






    def _get_word_from(self, word_address):
        with self.lock:
            offset = (word_address - 0xc000) * 2
            byte0 = self.memorymap[offset+1]
            byte1 = self.memorymap[offset+0]
            result = (byte1<<8) | byte0
            return result

    def update_comm_status(self):
        pass

    def update_properties():
        pass

    def read_485(self):
        try:
            alarm   = self.jbus.read_with_retry(self.id, 0xc000, 4) # for 52k
            error   = self.jbus.read_with_retry(self.id, 0xc010, 4) # for 52k
            measure = self.jbus.read_with_retry(self.id, 0xc020, 52) # for 52k
        except (ValueError, serialSerialException) as ex:
            return None
        return alarm, error, measure
        

    def sync_with_hardware(self):
        with self.lock:
            if self.reset_counts:
                self.total_comm_counts = 0
                self.success_comm_counts = 0
                self.reset_counts = False

            self.total_comm_counts += 1 

        try:
            alarm   = self.jbus.read_with_retry(self.id, 0xc000, 4) # for 52k
            error   = self.jbus.read_with_retry(self.id, 0xc010, 4) # for 52k
            measure = self.jbus.read_with_retry(self.id, 0xc020, 52) # for 52k
        except ValueError as ex:
            print('Exception in {} sync_with_hardware(), {}'.format(str(self), repr(ex)))
            self.online = False 
            return
        except (serial.SerialException, Exception) as ex:
            print('Exception in {} sync_with_hardware(), {}'.format(str(self), repr(ex)))
            self.online = False 
            return

        with self.lock:
            # 7.2k night mode filter
            if self.is_7k2_night_mode(measure):
                print('Night Mode, SKIP')
                self.online = False 
                return

            # backup event code
            oldalarmcode = self.alarm
            olderrorcode = self.error

            # fill memory condition: all communication success
            # update memory mapping
            offset = 3
            payload = alarm[offset:-2]
            for i, v in enumerate(payload):
                idx = (0xc000-0xc000)*2 + i
                self.memorymap[idx] = v

            payload = error[offset:-2]
            for i, v in enumerate(payload):
                idx = (0xc010-0xc000)*2 + i
                self.memorymap[idx] = v

            payload = measure[offset:-2]
            for i, v in enumerate(payload):
                idx = (0xc020-0xc000)*2 + i
                self.memorymap[idx] = v

            self.last_update_timestamp = self.time()
            self.online = True
            self.notify()
            self.success_comm_counts += 1 

            self.process_alarm_queue(oldalarmcode, self.alarm)
            self.process_error_queue(olderrorcode, self.error)
            #self.handle_alarm_event_logs()
            #self.handle_error_event_logs()

            self.write_timestamp_to_real_inverter()

    def handle_alarm_event_logs(self):
        self.alarm_event_handler.input(self.alarm)
        records = self.alarm_event_handler.output()
        if records:
            [self.alarm_fifo.append(r) for r in records]

    def handle_error_event_logs(self):
        self.error_event_handler.input(self.error)
        records = self.error_event_handler.output()
        if records:
            [self.error_fifo.append(r) for r in records]

    def write_timestamp_to_real_inverter(self):
        # write timestamp to pv (for 25.6K) every 30 min and online event
        if self.online_event_occur:
            self.write_timecode_to_25k6_hardware()
            self.online_event_occur = False
            print('{} online event, write timestamp'.format(self)) 

        if self.time() - self.tm_jbus_write_timestamp > (30*60):
            self.write_timecode_to_25k6_hardware()
            print('{} every 30 mins, write timestamp'.format(self)) 


    def is_7k2_night_mode(self, measure):
            mstring = ' '.join(['{:02x}'.format(b) for b in measure])
            #print('measure: {}'.format(mstring))

            # kwh, 0xc031:0xc032, 34, 35, 36, 37 big-endian, offset 3
            kwh = measure[37] << 24 | measure[38] << 16 | measure[39] << 8 | measure[40]
            #print('kwh: {}'.format(kwh))

            # dc_positive, 0xc027, offset 3
            dc_positive = measure[17] << 8 | measure[18]
            #print('dc positive: {}'.format(dc_positive))

            # dc_negative, 0xc028, offset 3
            dc_negative = measure[19] << 8 | measure[20]
            #print('dc negative: {}'.format(dc_positive))

            # dc1, 0xc02b, offset 3
            dc1 = measure[25] << 8 | measure[26]
            #print('dc1 : {}'.format(dc1))

            # dc2, 0xc02c, offset 3
            dc2 = measure[27] << 8 | measure[28]
            #print('dc2 : {}'.format(dc2))

            #print('Night Mode ? {}, {}, {}, {}, {}'.format(dc1, dc2, dc_positive, dc_negative, kwh))
            if (dc1 == 0 and dc2 == 0 and dc_positive == 0 and dc_negative == 0 and kwh == 0):
                return True
            else:
                return False


    def update_statistics(self):
        self._OutputPower_fifo.append(self.OutputPower) 

        self._ACVolPhaseA_fifo.append(self.ACVolPhaseA)
        self._ACVolPhaseB_fifo.append(self.ACVolPhaseB)
        self._ACOutputCurrentA_fifo.append(self.ACOutputCurrentA)
        self._ACOutputCurrentB_fifo.append(self.ACOutputCurrentB)

        self._ACFrequency_fifo.append(self.ACFrequency)

        self._DCBusPositiveVol_fifo.append(self.DCBusPositiveVol)
        self._DCBusNegativeVol_fifo.append(self.DCBusNegativeVol)

        self._InternalTemper_fifo.append(self.InternalTemper) 
        self._HeatSinkTemper_fifo.append(self.HeatSinkTemper) 

        self._DC1InputVol_fifo.append(self.DC1InputVol) 
        self._DC2InputVol_fifo.append(self.DC2InputVol)
        self._DC1InputCurrent_fifo.append(self.DC1InputCurrent)
        self._DC2InputCurrent_fifo.append(self.DC2InputCurrent)

        self._InputPowerA_fifo.append(self.InputPowerA) 
        self._InputPowerB_fifo.append(self.InputPowerB) 
        self._TotalOutputPower_fifo.append(self.TotalOutputPower) 

        self._ACVolPhaseC_fifo.append(self.ACVolPhaseC) 
        self._ACOutputCurrentC_fifo.append(self.ACOutputCurrentC) 

        self._DC3InputVol_fifo.append(self.DC3InputVol) # for 52k
        self._DC4InputVol_fifo.append(self.DC4InputVol) # for 52k
        self._DC3InputCurrent_fifo.append(self.DC3InputCurrent) # for 52k
        self._DC4InputCurrent_fifo.append(self.DC4InputCurrent) # for 52k
        self._InputPowerC_fifo.append(self.InputPowerC) # for 52k
        self._InputPowerD_fifo.append(self.InputPowerD) # for 52k


    def read_cached_measurement(self):
        result = Measurement(self.id, datetime.datetime.now())
        result.OutputPower = self.OutputPower
        result.ACVolPhaseA = self.ACVolPhaseA 
        result.ACVolPhaseB = self.ACVolPhaseB 
        result.ACVolPhaseC = self.ACVolPhaseC 
        result.ACFrequency = self.ACFrequency
        result.ACOutputCurrentA = self.ACOutputCurrentA
        result.ACOutputCurrentB = self.ACOutputCurrentB
        result.ACOutputCurrentC = self.ACOutputCurrentC
        result.DC1InputVol = self.DC1InputVol
        result.DC2InputVol = self.DC2InputVol
        result.DC1InputCurrent = self.DC1InputCurrent
        result.DC2InputCurrent = self.DC2InputCurrent
        result.DCBusPositiveVol = self.DCBusPositiveVol 
        result.DCBusNegativeVol = self.DCBusNegativeVol 
        result.InternalTemper = self.InternalTemper 
        result.HeatSinkTemper = self.HeatSinkTemper 
        result.InputPowerA = self.InputPowerA
        result.InputPowerB = self.InputPowerB
        result.TotalOutputPower = self.TotalOutputPower 
        return result


class OnlineEvent(object):
    pass

class OfflineEvent(object):
    pass

class AlarmEvent(object):
    def __init__(self, who, oldcode, newcode, when):
        self.who = who
        self.when = when
        self.oldcode = oldcode
        self.newcode = newcode

    def records(self):
        result = []
        ALARM_TYPECODE = 1
        bitmask = 0x01
        #for shift in range(0, 48):
        for shift in range(0, 64): # for 52k
            b1 = self.newcode & (bitmask << shift)
            b2 = self.oldcode & (bitmask << shift)
            if b1 != b2:
                msg = "{id},{tf},{typecode},{bitnum},{stat}".format(
                    id=self.who,
                    tf=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.when)),
                    typecode=ALARM_TYPECODE,
                    bitnum=shift, 
                    stat='H' if b1 else 'R') 
                result.append(msg)
        return result


class ErrorEvent(object):
    def __init__(self, who, oldcode, newcode, when):
        self.who = who 
        self.when = when
        self.oldcode = oldcode
        self.newcode = newcode

    def records(self):
        result = []
        ERROR_TYPECODE = 2
        bitmask = 0x01
        #for shift in range(0, 48):
        for shift in range(0, 64): # for 52k
            b1 = self.newcode & (bitmask << shift)
            b2 = self.oldcode & (bitmask << shift)
            if b1 != b2:
                msg = "{id},{tf},{typecode},{bitnum},{stat}".format(
                    id=self.who,
                    tf=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(self.when)),
                    typecode=ERROR_TYPECODE,
                    bitnum=shift, 
                    stat='H' if b1 else 'R') 
                result.append(msg)
        return result


class Measurement(object):
    def __init__(self, mid, datetime):
        self.mid = mid
        self.datetime = datetime
        self.OutputPower = 0
        self.ACVolPhaseA = 0
        self.ACVolPhaseB = 0
        self.ACVolPhaseC = 0
        self.ACFrequency = 0
        self.ACOutputCurrentA = 0
        self.ACOutputCurrentB = 0
        self.ACOutputCurrentC = 0
        self.DC1InputVol = 0
        self.DC2InputVol = 0
        self.DC1InputCurrent = 0
        self.DC2InputCurrent = 0
        self.DCBusPositiveVol = 0
        self.DCBusNegativeVol = 0
        self.InternalTemper = 0
        self.HeatSinkTemper = 0
        self.InputPowerA = 0
        self.InputPowerB = 0
        self.TotalOutputPower = 0

    def __str__(self):
        return '{},{},...,{} KWH'.format( self.mid, 
                                          self.datetime.replace(microsecond=0), 
                                          round(self.TotalOutputPower,3))


class AblerexCloudEventTypeCode(Enum):
    STATUS = '0'
    ALARM  = '1'
    ERROR  = '2'



class EventHandler(object):
    def __init__(self, id, typecode):
        self.id = id
        self.fifo = collections.deque(maxlen=2)
        self.fifo.append(0x00)
        self.typecode = typecode
        self.init_datetime = datetime.datetime.now()
        pass

    def input(self, code):
        delta = datetime.datetime.now() - self.init_datetime
        if delta.seconds > (60*6):
            self.fifo.append(code)

    def output(self):
        try:
            result = []
            oldcode = self.fifo[0]
            newcode = self.fifo[1]
            ALARM_TYPECODE = 1
            bitmask = 0x01
            for shift in range(0, 64):
                b1 = newcode & (bitmask << shift)
                b2 = oldcode & (bitmask << shift)
                if b1 != b2:
                    msg = "{id},{tf},{typecode},{bitnum},{stat}".format(
                        id=self.id,
                        tf=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                        typecode=self.typecode,
                        bitnum=shift, 
                        stat='H' if b1 else 'R') 
                    result.append(msg)
            return result
        except IndexError as err:
            pass

        

if __name__ == '__main__':
    #ae = AlarmEvent(1, 0x00, 0x01, time.time())
    #print(ae.records())
    aeh = EventHandler(1, AblerexCloudEventTypeCode.ALARM.value)

    fake_datetime = datetime.datetime.now() - datetime.timedelta(minutes=7)
    aeh.init_datetime = fake_datetime


    aeh.input(0x01)
    logs = aeh.output()
    print(logs)

    aeh.input(0x00)
    logs = aeh.output()
    print(logs)

