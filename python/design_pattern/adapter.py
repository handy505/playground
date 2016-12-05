#!/usr/bin/env python3

class Machine(object):
    def __init__(self):
        self.val = 0

class Adapter(object):
    def __init__(self, machine):
        self.machine = machine
        self._val = None

    @property
    def val(self):
        v = self.machine.val
        if v == 0:
            return '#'
        else:
            return v

    @val.setter
    def val(self, arg):
        self.machine.val = arg


if __name__ == '__main__':
    m = Machine()
    m.val = 0
    print(m.val)
    m.val = 9
    print(m.val)

    am = Adapter(m)
    am.val = 0
    print(am.val)
    am.val = 9
    print(am.val)

'''output 
0
9
#
9
'''
    