#!/usr/bin/env python3

import collections

class Machine(object):
    def __init__(self):
        self.val = 0


class Proxy(object):
    def __init__(self, machine):
        self.machine = machine
        self._val = self.machine.val
        self.fifo = collections.deque()
        self._avg = None

    @property
    def val(self):
        return self.machine.val

    @val.setter
    def val(self, arg):
        self.machine.val = arg
        self.fifo.append(arg)
        if len(self.fifo) > 8: self.fifo.popleft()

    @property
    def avg(self):
        return sum(self.fifo)/len(self.fifo)


if __name__ == '__main__':
    m = Machine()
    
    p = Proxy(m)
    p.val = 0
    print(p.val)
    p.val = 8
    print(p.val)
    print(p.avg)

'''output 
0
8
4.0
'''
    