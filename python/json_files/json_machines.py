#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Do NOT use user filename as json.py
# it used by python buildin module
# error: AttributeError: 'module' object has no attribute 'dumps'

import json
import collections

class MachineConfiguration(object):
    def __init__(self, id=1, port=None):
        self.id = id
        #self.voltage = 100
        #self.current = 50
        self.port = port

    def __repr__(self):
        return str(self.__dict__)


class SystemConfiguration(object):
    def __init__(self):
        self.mlist = []
        self.wifi_ssid = 'unknow_ssid'
        self.wifi_password = 'unknow_password'

    def __repr__(self):
        return str(self.__dict__)
    

def  object2dict(obj):
    #convert object to a dict
    dsc = {}
    dms = []
    for i, m in enumerate(obj.mlist):        
        dms.append(m.__dict__)

    dsc['machines'] = dms
    dsc['wifi_ssid'] = obj.wifi_ssid
    dsc['wifi_password'] = obj.wifi_password

    return  dsc


def  dict2object(d):
    sc = SystemConfiguration()
     
    for dmc in d['machines']:
        mc = MachineConfiguration()
        mc.id = dmc['id']
        mc.port = dmc['port']
        sc.mlist.append(mc)
    
    sc.wifi_ssid = d['wifi_ssid']
    sc.wifi_password = d['wifi_password'] 
    
    return sc



if __name__ == "__main__":
    
    sc = SystemConfiguration()
    for i in range(1,4):
        mc = MachineConfiguration(i, '/dev/ttyUSB0')
        sc.mlist.append(mc)
    sc.wifi_ssid = 'handyssid'
    sc.wifi_password = '1234567890'


    jsonstr = json.dumps(sc, sort_keys=True, default=object2dict, indent=4)
    print(jsonstr)
    with open('configurations.json', 'w', encoding='utf-8') as fw:
        fw.write(jsonstr)


    # json string to dictionary
    s = ''
    with open('configurations.json', 'r', encoding='utf-8') as fr:
        s = fr.read()


    d2 = json.loads(s)

    sc = dict2object(d2)
    print(sc)






