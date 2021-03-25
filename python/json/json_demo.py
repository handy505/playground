#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Do NOT use user filename as json.py
# it used by python buildin module
# error: AttributeError: 'module' object has no attribute 'dumps'

import json
import collections

class Machine(object):
    def __init__(self):
        self.id = 1
        self.voltage = 100
        self.current = 50


if __name__ == "__main__":
    m1 = Machine()
    print(m1)
    print(m1.__dict__)

    # dictionary to json string
    jsonstr = json.dumps(m1.__dict__)
    print(jsonstr)

    # dictionary to json string
    jsonstr = json.dumps(m1.__dict__, sort_keys=True)
    print(jsonstr)

    # dictionary to json string
    d = collections.OrderedDict()
    d["id"] = m1.id
    d["voltage"] = m1.voltage
    d["current"] = m1.current
    jsonstr = json.dumps(d)
    print(jsonstr)

    # json string to dictionary
    j2 = json.loads(jsonstr)
    print('j2: {}, {}, {}'.format(j2['id'], j2['voltage'], j2['current']))

    # check the key is valid
    if 'id' in j2.keys(): 
        print('ok')
    else:
        print('not exist')


