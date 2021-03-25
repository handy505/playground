#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import crc

def read_memory_by_modbus(deviceid, memorymap, querypacket):
    if len(querypacket) < 6:
        return None

    slavenumber  =  querypacket[0]
    functioncode =  querypacket[1]
    address      = (querypacket[2] << 8) + querypacket[3]
    wordlength   =  querypacket[5]

    # id check
    if slavenumber != deviceid:
        #print('ID error')
        return None

    # crc check
    if not crc.check_crc16(querypacket):
        #print('CRC error')
        return None

    # function code check
    if functioncode != 3:
        print('Not support function code {}'.format(functioncode))
        return None

    # address check
    if not address >= memorymap.start_address:
        #print('address error')
        return None

    if not ((address+wordlength) <= memorymap.end_address):
        #print('address error')
        return None

    # prepare response
    resphex = '{:02x} {:02x} {:02x}'.format(slavenumber, 
                                            functioncode, 
                                            wordlength*2)
    header = bytearray.fromhex(resphex)

    # prepare payload
    data = memorymap.dump(address, wordlength)
    d = ' '.join(['{:04x}'.format(b) for b in data])
    data = bytearray.fromhex(d)

    resp = header + data
    resp = crc.append_crc16(resp)
    return resp


def dumphex(pkt):
    result = ' '.join(['{:02x}'.format(b) for b in pkt]) # debug
    return result


if __name__ == '__main__':

    from memorymapping import MemoryMapping
    mm = MemoryMapping(0xC000, 0xC07F) 
    mm.write(0xC000, 100)


    hexstr = '01 03 C0 00 00 01 B8 0A'
    pkt = bytearray.fromhex(hexstr)

    resp = read_memory_by_modbus(1, mm, pkt)
    print(dumphex(resp))


