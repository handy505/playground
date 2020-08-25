#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import crc
import time
import optparse
import sys


def show_packet(packet):
    result = ' '.join(['{:02x}'.format(b) for b in packet])
    return result

def read_fw_version(mid, ser):
    hexstr = '{:02x} 03 c0 bc 00 04'.format(mid)
    ba = bytearray.fromhex(hexstr)
    txpacket = crc.append_crc16(ba)

    ser.reset_output_buffer()
    ser.reset_input_buffer()
    print('tx: {}'.format(show_packet(txpacket)))
    ser.write(txpacket)
    ser.flush()
    time.sleep(0.2) # wait for machine processing 
    time.sleep(1) # force wait
    rxpacket = ser.read(ser.in_waiting)
    #print('rx: {}'.format(show_packet(rxpacket)))
    if crc.check_crc16(rxpacket):
        result = rxpacket[3:-2].decode('utf-8')
        return result 


def get_typename(fwcode):
    code = fwcode[4:6]
    result = 'unknow'
    if code == '82':   result = '52k'
    elif code == '60': result = '25.6k'
    elif code == '07': result = '12k'
    elif code == '70': result = '7.2k'
    elif code == '66': result = 'ESJ5500'
    elif code == '46': result = '5k'

    return result



if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option(
        '-i', '--id',
        type='int',
        dest='id',
        help='PV Inverter ID')
    parser.add_option(
        "-t", "--to",
        dest="to",
        type="int",
        help="To Inverter ID [default=%default]")
    parser.add_option(
        "-s", 
        "--serialport",
        type="string",
        dest="serialport",
        default='/dev/ttyUSB0',
        help="Indicate serial port")
    opts, args = parser.parse_args()

    if not opts.id:
        print('Parameter error: must indicate device ID')
        sys.exit() 

    if not opts.to: to = opts.id
    else:           to = opts.to

    ser = serial.Serial(port=opts.serialport, baudrate=9600, timeout=0.8)

    for mid in range(opts.id, to+1):
        result = read_fw_version(mid, ser)
        if result:
            typename = get_typename(result)
            print('ID-{} Firmware version: {}, {}'.format(mid, result, typename))
        else:
            print('ID-{} no response'.format(mid))

