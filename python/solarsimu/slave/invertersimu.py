#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modbus_slave_controller import read_memory_by_modbus
from memorymapping import MemoryMapping


def dumphex(pkt):
    result = ' '.join(['{:02x}'.format(b) for b in pkt]) # debug
    return result


class InverterSimulator(object):
    def __init__(self, id):
        self.id = id
        self.mm = MemoryMapping(0xC000, 0xC060)

        self.alarm_code = 0x00
        self.error_code = 0x00

        self.dc1_voltage = 800
        self.dc2_voltage = 800
        self.dc3_voltage = 800
        self.dc4_voltage = 800

        self.dc1_current = 10
        self.dc2_current = 10
        self.dc3_current = 10
        self.dc4_current = 10

        self.dc_positive = 1000
        self.dc_negative = 0

        self.internal_temp = 90
        self.heatsink_temp = 80 
        
        self.ac1_voltage = 230
        self.ac2_voltage = 230
        self.ac3_voltage = 230

        self.ac1_current = 10
        self.ac2_current = 10
        self.ac3_current = 10

        self.ac_frequency = 60
        self.ac_output_power = 5000
        self.kwh = 9000

        # fill to memory
        self.mm.write(0xC02B, self.dc1_voltage)
        self.mm.write(0xC02C, self.dc2_voltage)
        self.mm.write(0xC04E, self.dc3_voltage)
        self.mm.write(0xC04F, self.dc4_voltage)
        
        self.mm.write(0xC02D, self.dc1_current)
        self.mm.write(0xC02E, self.dc2_current)
        self.mm.write(0xC050, self.dc3_current)
        self.mm.write(0xC051, self.dc4_current)

        self.mm.write(0xC027, self.dc_positive)
        self.mm.write(0xC028, self.dc_negative)

        self.mm.write(0xC029, self.internal_temp)
        self.mm.write(0xC02A, self.heatsink_temp)
        
        self.mm.write(0xC021, self.ac1_voltage)
        self.mm.write(0xC022, self.ac2_voltage)
        self.mm.write(0xC03E, self.ac3_voltage)

        self.mm.write(0xC024, self.ac1_current)
        self.mm.write(0xC025, self.ac2_current)
        self.mm.write(0xC041, self.ac3_current)

        self.mm.write(0xC026, self.ac_frequency)
        self.mm.write(0xC020, self.ac_output_power)

        kwh_high_word = (self.kwh >> 16) & 0xffff
        kwh_low_word  =  self.kwh & 0xffff
        self.mm.write(0xc031, kwh_high_word)
        self.mm.write(0xc032, kwh_low_word)


    def __str__(self):
        return 'Inverter-{}'.format(self.id)

    def read_memory_by_modbus(self, pkt):
        result = read_memory_by_modbus(1, self.mm, pkt)
        '''if result:
            print(dumphex(result))
            '''
        return result

if __name__ == '__main__':
    inv = InverterSimulator(29)
    print(inv)
    print(inv.kwh)
    print(hex(inv.mm.read(0xC031)))
    print(hex(inv.mm.read(0xC032)))
