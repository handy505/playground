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
    #ser1 = serial.Serial(port='COM1', baudrate=115200, timeout=0.8)
    ser1 = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.8)

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
        #print(hexdump(txpacket))

        ser1.reset_output_buffer()
        ser1.reset_input_buffer()
        ser1.write(txpacket)
        ser1.flush()
        time.sleep(0.1) # wait for machine processing 
        rxpacket = ser1.read(ser1.in_waiting)
        #print(hexdump(rxpacket))



    #ser2 = serial.Serial(port='COM2', baudrate=921600, timeout=0.8)
    ser2 = serial.Serial(port='/dev/ttyACM1', baudrate=921600, timeout=0.8)
    while True:
        rxpacket = ser2.read(ser2.in_waiting)
        if rxpacket:
            print(hexdump(rxpacket))
            #print(len(rxpacket))
            #print(type(rxpacket))
            parse_rxpacket(rxpacket)
            print('--------')
        time.sleep(0.1)


def parse_rxpacket(rxpacket):
    packetcount = 0
    try:
        q = deque(maxlen=40)
        for i, b in enumerate(rxpacket):
            q.append(b)
            if len(q) >= 40:
                if (q[0] == 0x02 and 
                    q[1] == 0x01 and 
                    q[2] == 0x04 and 
                    q[3] == 0x03 and 
                    q[4] == 0x06 and 
                    q[5] == 0x05 and 
                    q[6] == 0x08 and 
                    q[7] == 0x07):
                    
                    packetcount += 1

                    print('--------')
                    header = (q[0] << 56 | 
                              q[1] << 48 | 
                              q[2] << 40 | 
                              q[3] << 32 | 
                              q[4] << 24 | 
                              q[5] << 16 | 
                              q[6] << 8  | 
                              q[7])
                    print('header: 0x{:016X}, i={}'.format(header, i))
                    
                    version = (q[11] << 24 | 
                               q[10] << 16 | 
                               q[9]  << 8  | 
                               q[8])
                    print('version: 0x{:08X}'.format(version)) 

                    totalPacketLen= (q[15] << 24 | 
                                     q[14] << 16 | 
                                     q[13] << 8  | 
                                     q[12])
                    print('totalPacketLen: {}({:08X})'.format(totalPacketLen, totalPacketLen)) 
                    
                    platform = (q[19] << 24 | 
                                q[18] << 16 | 
                                q[17] << 8  | 
                                q[16])
                    print('platform: {}({:08X})'.format(platform, platform)) 

                    frameNumber = (q[23] << 24 | 
                                   q[22] << 16 | 
                                   q[21] << 8  | 
                                   q[20])
                    print('frameNumber: {}({:08X})'.format(frameNumber, frameNumber)) 

                    timeCpuCycles = (q[27] << 24 | 
                                     q[26] << 16 | 
                                     q[25] << 8  | 
                                     q[24])
                    print('timeCpuCycles: {}({:08X})'.format(timeCpuCycles, timeCpuCycles)) 

                    numDetectedObj = (q[31] << 24 | 
                                      q[30] << 16 | 
                                      q[29] << 8  | 
                                      q[28])
                    print('numDetectedObj: {}({:08X})'.format(numDetectedObj, numDetectedObj)) 

                    numTLVs = (q[35] << 24 | 
                               q[34] << 16 | 
                               q[33] << 8  | 
                               q[32])
                    print('numTLVs: {}({:08X})'.format(numTLVs, numTLVs)) 

                    subFrameIndex = (q[39] << 24 | 
                                     q[38] << 16 | 
                                     q[37] << 8  | 
                                     q[36])
                    print('subFrameIndex: {}({:08X})'.format(subFrameIndex, subFrameIndex)) 


        print('packetcount: {}'.format(packetcount))
    except IndexError as err:
        print(err)

    return len(rxpacket)


if __name__ == '__main__':
    main()


    '''pkt = '02 01'
    count_frame_header(pkt)
    '''
