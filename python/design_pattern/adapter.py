#!/usr/bin/env python3

class Machine(object):
    def __init__(self):
        self.output_power = 0

class UnitAdapter(object):
    def __init__(self, machine):
        self.machine = machine
        self._output_power = None

    @property
    def output_power(self):
        p = self.machine.output_power/10
        return p

    @output_power.setter
    def val(self, arg):
        self.machine.val = arg


if __name__ == '__main__':
    m = Machine()
    m.output_power = 1234
    print(m.output_power)

    am = UnitAdapter(m)
    print(am.output_power)
    

'''output 
1234
123.4
'''
    