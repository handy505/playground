#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import random
from datetime import datetime


def create_gateway_channel(name):
    result = {'display_name': name,
              'properties': { 'data_type': 'STRING',
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


def create_inverter_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': {'DC1Voltage': create_voltage_channel('DC1Voltage'),
                      'DC2Voltage': create_voltage_channel('DC2Voltage'),
                      'DC3Voltage': create_voltage_channel('DC3Voltage'),
                      'DC4Voltage': create_voltage_channel('DC4Voltage'),

                      'DC1Current': create_current_channel('DC1Current'),
                      'DC2Current': create_current_channel('DC2Current'),
                      'DC3Current': create_current_channel('DC3Current'),
                      'DC4Current': create_current_channel('DC4Current'),

                      'DC1Power': create_power_channel('DC1Power'),
                      'DC2Power': create_power_channel('DC2Power'),
                      'DC3Power': create_power_channel('DC3Power'),
                      'DC4Power': create_power_channel('DC4Power'),

                      'DCPositive': create_basic_channel('DCPositive'),
                      'DCNegative': create_basic_channel('DCNegative'),

                      'InternalTemp': create_basic_channel('InternalTemp'),
                      'HeatSinkTemp': create_basic_channel('HeatSinkTemp'),

                      'AC1Voltage': create_basic_channel('AC1Voltage'),
                      'AC2Voltage': create_basic_channel('AC2Voltage'),
                      'AC3Voltage': create_basic_channel('AC3Voltage'),

                      'AC1Current': create_basic_channel('AC1Current'),
                      'AC2Current': create_basic_channel('AC2Current'),
                      'AC3Current': create_basic_channel('AC3Current'),

                      'ACFrequency': create_basic_channel('ACFrequency'),
                      'ACOutputPower': create_basic_channel('ACOutputPower'),
                      'KWH': create_basic_channel('KWH'),

                     },
        }
    return d



def create_meter_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': { 'Value': create_basic_channel('Value') }
        }
    return d

def create_gateway_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': { 'MAC': create_gateway_channel('MAC'), 
                       'ServiceID': create_gateway_channel('ServiceID'), 
                     }
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


if __name__ == '__main__':
    pass
