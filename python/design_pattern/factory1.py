#!/usr/bin/env python3

class PV(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'i am pv{}'.format(self.id)

class Taurus(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'i am taurus{}'.format(self.id)

class SimpleFactory(object):
    def __init__(self):
        pass

    def get_instance(self, type, arg):
        if type == 'pv': return PV(arg)
        elif type == 'taurus': return Taurus(arg)
        else: print('error argument')

if __name__ == '__main__':

    a = PV(1)
    b = PV(2)
    c = Taurus(3)
    d = Taurus(4)
    print(a)
    print(b)
    print(c)
    print(d)
    
    fac = SimpleFactory()
    e = fac.get_instance('pv', 5)
    f = fac.get_instance('taurus', 6)
    print(e)
    print(f)
    