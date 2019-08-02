#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import random
from datetime import datetime

def create_json_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type':      'JSON',
                              'primitive_type': 'JSON',
                            }
             }
    return result 

def create_string_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type':      'STRING',
                              'primitive_type': 'STRING',
                            }
             }
    return result 


def create_basic_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type': 'ELEC_POTENTIAL',
                              'primitive_type': 'NUMERIC',
                              'precision': 1,
                            }
             }
    return result 


def create_voltage_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type': 'ELEC_POTENTIAL',
                              'primitive_type': 'NUMERIC',
                              'data_unit': 'V',
                              'precision': 1,
                            }
             }
    return result 


def create_current_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type': 'ELEC_CURRENT',
                              'primitive_type': 'NUMERIC',
                              'data_unit': 'A',
                              'precision': 1,
                            }
             }
    return result 


def create_power_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type': 'ENERGY',
                              'primitive_type': 'NUMERIC',
                              'data_unit': 'KWH',
                              'precision': 1,
                            }
             }
    return result 

# ----------------------------------------------------------------------------
def create_inverter_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'

    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': {'LoggedTime': create_string_channel('LoggedTime'),
                      'Events'    : create_string_channel('Events'),
                      'InputSide' : create_json_channel('InputSide'),
                      'OutputSide': create_json_channel('OutputSide'),
                      'Internal'  : create_json_channel('Internal'),
                      'ACOutputPower': create_basic_channel('ACOutputPower'),
                      'KWH': create_basic_channel('KWH'),
                     },
        }
    return d



def create_inverter_record_dict(rec):
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'

    inputside = { 'headers': ['DC1Voltage', 'DC2Voltage', 'DC3Voltage', 'DC4Voltage', 'DC1Current', 'DC2Current', 'DC3Current', 'DC4Current'],
                  'values': [[ rec.DC1Voltage, 
                               rec.DC2Voltage,
                               rec.DC3Voltage,
                               rec.DC4Voltage,
                               rec.DC1Current,
                               rec.DC2Current,
                               rec.DC3Current,
                               rec.DC4Current,
                            ]]
                }

    internal = { 'headers': ['DCPositive', 'DCNegative', 'InternalTemp', 'HeatSinkTemp'],
                 'values':  [[rec.DCPositive, 
                              rec.DCNegative, 
                              rec.InternalTemp, 
                              rec.HeatSinkTemp
                            ]]
               }


    outputside = { 'headers': ['AC1Voltage', 'AC2Voltage', 'AC3Voltage', 'AC1Current', 'AC2Current', 'AC3Current', 'ACFrequency'],
                   'values':  [[rec.AC1Voltage, 
                                rec.AC2Voltage, 
                                rec.AC3Voltage, 
                                rec.AC1Current, 
                                rec.AC2Current, 
                                rec.AC3Current, 
                                rec.ACFrequency
                              ]]
                 }               

    d = {'LoggedTime'   : isodt,
         'Events'       : rec.Events,
         'InputSide'    : inputside,
         'Internal'     : internal,
         'OutputSide'   : outputside,
         'ACOutputPower': rec.ACOutputPower,
         'KWH'          : rec.KWH 
        }
    return d


def create_inverter_record_dict_old(rec):
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'LoggedTime': isodt,
         'DC1Voltage': rec.DC1Voltage,
         'DC2Voltage': rec.DC2Voltage,
         'DC3Voltage': rec.DC3Voltage,
         'DC4Voltage': rec.DC4Voltage,
         'DC1Current': rec.DC1Current,
         'DC2Current': rec.DC2Current,
         'DC3Current': rec.DC3Current,
         'DC4Current': rec.DC4Current,
         'DC1Power'  : rec.DC1Power, 
         'DC2Power'  : rec.DC2Power, 
         'DC3Power'  : rec.DC3Power, 
         'DC4Power'  : rec.DC4Power, 

         'DCPositive'  : rec.DCPositive,
         'DCNegative'  : rec.DCNegative, 
         'InternalTemp': rec.InternalTemp, 
         'HeatSinkTemp': rec.HeatSinkTemp, 

         'AC1Voltage': rec.AC1Voltage, 
         'AC2Voltage': rec.AC2Voltage, 
         'AC3Voltage': rec.AC3Voltage,
         'AC1Current': rec.AC1Current,
         'AC2Current': rec.AC2Current, 
         'AC3Current': rec.AC3Current, 

         'ACFrequency'  : rec.ACFrequency,
         'ACOutputPower': rec.ACOutputPower,
         'KWH'          : rec.KWH 
        }
    return d
# ----------------------------------------------------------------------------
def create_meter_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': {'LoggedTime': create_string_channel('LoggedTime'),
                      'Value': create_basic_channel('Value'),
                     }
        }
    return d

def creatre_meter_record_dict(rec):
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'LoggedTime': isodt,
         'Value': rec.Value,
        }
    return d

# ----------------------------------------------------------------------------
def create_gateway_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': { 'ServiceInfo': create_string_channel('ServiceInfo') }
        }
    return d


def post_config_io(config_io_dict, token):
    s = json.dumps(config_io_dict)
    s = 'config_io=' + s

    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}

    response = requests.post(url, headers=headers, data=s)
    print(response)
    print(response.headers)
    print(response.text)


def post_to_exosence_data_in(d, token):
    s = json.dumps(d)
    s = 'data_in=' + s

    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    response = requests.post(url, headers=headers, data=s)
    print(response)

if __name__ == '__main__':
    pass
