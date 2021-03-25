import serial
import time
from collections import deque
import struct

def hexdump(src, length=16):
    '''
    reference to http://code.activestate.com/recipes/142812-hex-dumper/
    modity python2 to python3
    '''
    result = []
    digits = 4 if isinstance(src, bytes) else 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(['{:>02X}'.format(x) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        line = '{:>04} {:<48s} {}'.format(i, hexa, text)
        result.append(line) 
    return '\n'.join(result)


def main():
    print('hello mmwawve')
    ser1 = serial.Serial(port='COM1', baudrate=115200, timeout=0.8)

    lines = []
    with open('ods_default_config.cfg', 'r') as fd:
        for line in fd.readlines():
            lines.append(line)
            
    for line in lines:
        print(line)

    for line in lines:
        #print('[32mMaster: {}[m'.format(line))
        #txpacket = bytearray.fromhex(line)
        txpacket = bytearray(line, encoding='utf-8')
        print(hexdump(txpacket))

        ser1.reset_output_buffer()
        ser1.reset_input_buffer()
        ser1.write(txpacket)
        ser1.flush()
        time.sleep(0.1) # wait for machine processing 
        rxpacket = ser1.read(ser1.in_waiting)
        print(hexdump(rxpacket))



    ser2 = serial.Serial(port='COM2', baudrate=921600, timeout=0.8)
    while True:
        rxpacket = ser2.read(ser2.in_waiting)
        if rxpacket:
            print(hexdump(rxpacket))
            print(len(rxpacket))
            count_frame_header(rxpacket)
        time.sleep(0.5)

def count_frame_header(rxpacket):
    packetcount = 0
    try:
        q = deque(maxlen=40)
        for i, b in enumerate(rxpacket):
            q.append(b)
            if len(q) >= 40:
                if  q[0] == 0x02 and q[1] == 0x01 and q[2] == 0x04 and q[3] == 0x03 and q[4] == 0x06 and q[5] == 0x05 and q[6] == 0x08 and q[7] == 0x07:
                    
                    packetcount += 1

                    header = q[0] << 56 | q[1] << 48 | q[2] << 40 | q[3] << 32 | q[4] << 24 | q[5] << 16 | q[6] << 8 | q[7]
                    print('header: {}'.format(header))
                    
                    version = q[9] << 24 | q[8] << 16 | q[11] << 8 | q[10]
                    print('version: {:08X}'.format(version)) 


        print('debug: {}'.format(packetcount))
    except IndexError as err:
        print(err)

    return len(rxpacket)

if __name__ == '__main__':
    main()


    '''pkt = '02 01'
    count_frame_header(pkt)
    '''