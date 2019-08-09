#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import random
from datetime import datetime

def create_basic_channel(name, data_type='ELEC_POTENTIAL', primitive_type='NUMERIC'):
    result = {
        'display_name': name,
        'properties': { 
            'data_type': data_type,
            'primitive_type': primitive_type,
            'precision': 1,
        },
        'protocol_config':{
            'sample_rate': 60000,
            'report_rate': 60000,
            'timeout': 180000,
        },
    }
    return result 


# ----------------------------------------------------------------------------
def create_inverter_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': {'Events'       : create_basic_channel('Events', data_type='STRING', primitive_type='STRING'),
                      'Others'       : create_basic_channel('Others', data_type='JSON', primitive_type='JSON'),
                      'ACOutputPower': create_basic_channel('ACOutputPower'),
                      'KWH'          : create_basic_channel('KWH'),
                      'HourlyKWH'    : create_basic_channel('HourlyKWH'),
                     },
        }
    return d


def create_inverter_record_dict(rec):
    others = { 'headers': ['Key', 'Value'],
               'values':  [['DC1Voltage', rec.DC1Voltage],
                           ['DC2Voltage', rec.DC2Voltage],
                           ['DC3Voltage', rec.DC3Voltage],
                           ['DC4Voltage', rec.DC4Voltage],
                           ['DC1Current', rec.DC1Current],
                           ['DC2Current', rec.DC2Current],
                           ['DC3Current', rec.DC3Current],
                           ['DC4Current', rec.DC4Current],
                           ['DCPositive', rec.DCPositive],
                           ['DCNegative', rec.DCNegative],
                           ['InternalTemp', rec.InternalTemp],
                           ['HeatSinkTemp', rec.HeatSinkTemp],
                           ['AC1Voltage', rec.AC1Voltage],
                           ['AC2Voltage', rec.AC2Voltage],
                           ['AC3Voltage', rec.AC3Voltage],
                           ['AC1Current', rec.AC1Current],
                           ['AC2Current', rec.AC2Current],
                           ['AC3Current', rec.AC3Current],
                           ['ACFrequency',rec.ACFrequency],
                          ]
             }

    '''d = {'Events'       : rec.Events,
         'Others'       : others,
         'ACOutputPower': rec.ACOutputPower,
         'KWH'          : rec.KWH,
         'HourlyKWH'    : rec.HourlyKWH
        }'''
    d = {'Events'       : rec.Events,
         'Others'       : others,
         'ACOutputPower': rec.ACOutputPower,
         'KWH'          : rec.KWH,
        }
    return d


# ----------------------------------------------------------------------------
def create_meter_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': {'Value': create_basic_channel('Value')}
        }
    return d

def creatre_meter_record_dict(rec):
    d = {'Value': rec.Value}
    return d

# ----------------------------------------------------------------------------
def create_gateway_config_io():
    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': { 'ServiceInfo': create_basic_channel('ServiceInfo', data_type='STRING', primitive_type='STRING') }
        }
    return d


# ----------------------------------------------------------------------------
def post_config_to_exosense(config_io_dict, token):
    s = json.dumps(config_io_dict)
    s = 'config_io=' + s

    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    response = requests.post(url, headers=headers, data=s)
    print(response)


def post_data_to_exosence(d, token):
    s = json.dumps(d)
    s = 'data_in=' + s

    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    response = requests.post(url, headers=headers, data=s)
    print(response)


def post_dataout_to_exosense(config_io_dict, token):
    s = json.dumps(config_io_dict)
    s = 'data_out=' + s

    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    response = requests.post(url, headers=headers, data=s)
    print(response)

# ----------------------------------------------------------------------------
def get_timestamp():
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/timestamp'
    resp = requests.get(url)
    print(resp)
    print(resp.text)
    dt = datetime.fromtimestamp(int(resp.text))
    print(dt)
    print(dt.timestamp())


def long_polling():
    token = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias?hourlykwh'
    headers = {'Accept': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token,
               'Request-Timeout': '30000'}
    response = requests.get(url, headers=headers)
    print(response)


if __name__ == '__main__':
    #get_timestamp()
    #long_polling()

    token = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias?hourlykwh'
    headers = {'Accept': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    resp = requests.get(url, headers=headers)
    print(resp)
    print(resp.headers)
    print(resp.text)

    pass

