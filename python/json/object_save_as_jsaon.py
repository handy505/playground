#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import json
import random
import collections

class Inverter(object):
    def __init__(self, id):
        self.id = id 
        self.voltage = random.randint(100,120)
        self.current = random.randint(10,20) 
        self.KWH = random.randint(1000, 1100) 

    def __repr__(self):
        return 'Inverter-{}, {}V, {}A'.format(self.id, self.voltage, self.current)


if __name__ == "__main__":

    # create object
    inverters = [Inverter(id) for id in range(1,10)]
    [print(inv) for inv in inverters]


    # create snapshots
    inverter_snapshots = []
    for inv in inverters:
        jsonstr = json.dumps(inv.__dict__, sort_keys=True)
        print(jsonstr)
        inverter_snapshots.append(jsonstr)

    # save to file
    with open('inverters.tmp', 'w', encoding='utf-8') as fd:
        inverter_snapshots = [ line+'\n' for line in inverter_snapshots]
        fd.writelines(inverter_snapshots)
        

    # load from file
    snapshots = []
    with open('inverters.tmp', 'r', encoding='utf-8') as fd:
        for line in fd.readlines():
            d = json.loads(line) 
            print(type(d))
            print(d)
            snapshots.append(d)
    print(snapshots)


    # fill_Inverters_with_snapshots()


