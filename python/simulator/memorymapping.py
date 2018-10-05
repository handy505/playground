#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class MemoryMapping(object):

    def __init__(self, start_address, end_address):
        self.start_address = start_address
        self.end_address = end_address

        wordslength = self.end_address - self.start_address + 1
        #print('wordslength: {}'.format(wordslength))
        byteslength = wordslength * 2
        #print('byteslength: {}'.format(byteslength))

        self.memory = bytearray(byteslength)


    def read(self, word_address):
        offset = (word_address - self.start_address) * 2
        byte0 = self.memory[offset+0] # big-endian
        byte1 = self.memory[offset+1]
        result = (byte0<<8) | byte1
        return result


    def write(self, word_address, value):
        byte0 = value & 0xff
        byte1 = (value >> 8) & 0xff
        #offset = (word_address - 0xc000) * 2
        offset = (word_address - self.start_address) * 2
        self.memory[offset+0] = byte1
        self.memory[offset+1] = byte0


    def dump(self, start_address, length):
        result = []
        for offset in range(0, length):
            addr = start_address + offset
            w = self.read(addr)
            result.append(w)
        return result

    def memory_copy(self, addr, data):
        for i, v in enumerate(data):
            idx = (addr - self.start_address) * 2 + i # index of bytes
            self.memory[idx] = v
            



if __name__ == '__main__':

    mm = MemoryMapping(0xc000, 0xc020)

    for i, val in enumerate(mm.memory):
        mm.memory[i] = i


    w = mm.read(0xc000)
    #print('{:04x}'.format(w))
    w = mm.read(0xc001)
    #print('{:04x}'.format(w))


    ws = mm.dump(0xc000, 4)
    w = ' '.join(['{:04x}'.format(x) for x in ws])
    print(w)


    mm.write(0xc000, 0xabcd)


    ws = mm.dump(0xc000, 4)
    w = ' '.join(['{:04x}'.format(x) for x in ws])
    print(w)
