#!/usr/bin/env python3

class Machine(object):
    def __init__(self, id, brand='unknow'):
        self.id = id
        self.brand = brand

    def __str__(self):
        return '{}-{}'.format(self.brand, self.id)

    def read(self):
        pass


class AblerexPVInverter(Machine):
    def __init__(self, id):
        super().__init__(id, 'Ablerex')

    def read(self):
        print('{} read'.format(self.__str__()))


class DeltaPVInverter(Machine):
    def __init__(self, id):
        super().__init__(id, 'Delta')

    def read(self):
        print('{} read'.format(self.__str__()))


if __name__ == '__main__':

    machines = []
    machines.append(AblerexPVInverter(1))
    machines.append(DeltaPVInverter(2))
    
    [print(m) for m in machines]
    [m.read() for m in machines]

''' output:
Ablerex-1
Delta-2
Ablerex-1 read
Delta-2 read
'''
