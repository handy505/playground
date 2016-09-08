#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
#from collections import OrderedDict
import collections

class Machine(object):
    def __init__(self):
        self.id = 1
        self.voltage = 100
        self.current = 50


if __name__ == "__main__":
    m1 = Machine()
    print (m1)
    print(m1.__dict__)

    jsonstr = json.dumps(m1.__dict__)
    print(jsonstr)

    jsonstr = json.dumps(m1.__dict__, sort_keys=True)
    print(jsonstr)

    d = collections.OrderedDict()
    d["id"] = m1.id
    d["voltage"] = m1.voltage
    d["current"] = m1.current
    jsonstr = json.dumps(d)
    print(jsonstr)

