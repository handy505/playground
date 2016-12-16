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


class SystemConfiguration(object):
    def __init__(self):
        self.mlist = []
        self.wifi_ssid = 'unknow_ssid'
        self.wifi_password = 'unknow_password'

    
        


'''def  object2dict(obj):
    #convert object to a dict
    d = {}
    d[ '__class__' ] =  obj.__class__.__name__
    d[ '__module__' ] =  obj.__module__
    d.update(obj.__dict__)
    return  d'''


def  object2dict(obj):
    #convert object to a dict
    dsc = {}
    dms = []
    for i, m in enumerate(obj.mlist):
        '''dm = {}
        dm.update(m.__dict__)
        k = 'machine-{}'.format(m.id)
        dms[k] = m.__dict__'''

        
        dms.append(m.__dict__)
        dsc['machines'] = dms

    #dsc['machines'] = dms
    
    dsc['wifi_ssid'] = obj.wifi_ssid
    dsc['wifi_password'] = obj.wifi_password
    

    return  dsc


 
def  dict2object(d):
    #convert dict to object
    if '__class__'  in  d:
        class_name =  d.pop( '__class__' )
        module_name =  d.pop( '__module__' )
        module =  __import__ (module_name)
        class_  =  getattr (module,class_name)
        args =  dict ((key.encode( 'ascii' ), value) for  key, value in  d.items()) #get args
        inst =  class_ ( **args) #create new instance
    else :
        inst =  d
    return  inst



if __name__ == "__main__":
    
    sc = SystemConfiguration()
    for i in range(1,6):
        mc = MachineConfiguration(i, '/dev/ttyUSB0')
        sc.mlist.append(mc)


    #d = object2dict(sc)


    #print('{}'.format(d))

    jsonstr = json.dumps(sc, sort_keys=True, indent=4, default=object2dict)
    print(jsonstr)
    #print(repr(mg.__dict__))



    '''jsonstr = json.dumps(mg.__dict__, sort_keys=True, indent=2)
    print(jsonstr)

    jsonstr = json.dumps(m.__dict__, sort_keys=True)
    print(jsonstr)'''


    '''# dictionary to json string
    d = collections.OrderedDict()
    d["id"] = m.id
    d["voltage"] = m.voltage
    d["current"] = m.current
    jsonstr = json.dumps(d)
    print(jsonstr)'''

    # json string to dictionary
    sc2 = json.loads(jsonstr)
    print('sc2: {}, {}'.format(sc2['wifi_password'], sc2['wifi_ssid']))



