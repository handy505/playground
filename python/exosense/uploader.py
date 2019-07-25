#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import random
from datetime import datetime

def postman():
    d = {'id': 1, 'voltage': 100, 'current': 10}
    print(d)

    s = json.dumps(d)
    print(s)
    s = 'data_in=' + s
    print(s)

    #resp = requests.post(url, data=data)

    '''url = 'https://postman-echo.com/get?foo1=bar1&foo2=bar2'
    payload = {}
    headers = {}
    response = requests.request('GET', url, headers=headers, data=payload, allow_redirects=False, timeout=None)
    print(response.text)
    '''
    url = 'https://postman-echo.com/post'
    payload = s
    #headers = {}
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
    #response = requests.request('POST', url, headers=headers, data=payload)
    response = requests.post(url, headers=headers, data=payload)
    #print(response)
    print(response.headers)
    #print(response.text)


def activate():
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/provision/activate'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8'
              }
    data = 'id=Ablerex_001'
    response = requests.post(url, headers=headers, data=data)
    print(response)
    print(response.text)



def post_config_io():
    ch = {'display_name': 'Temperature',
          'description': 'Temperature Sensor Reading',
          'properties': { 'data_type': 'TEMPERATURE',
                           'primitive_type': 'NUMERIC',
                           'data_unit': 'DEG_CELSIUS',
                           'precision': 2,
                           'min': 16,
                           'max': 35,
                           'device_diagnostic': False,
                           'locked': True
                        },
          'protocol_config': { 'sample_rate': 2000,
                               'report_rate': 10000,
                               'down_sample': 'AVG',
                               'report_on_change': False,
                               'timeout': 300000,
                               'application': 'Modbus_RTU',
                               'interface': '/dev/tty0/',
                               'app_specific_config': {},
                               'input_raw': { 'max': 0,
                                              'min': 20,
                                              'unit': 'mA'
                                            }
                              }
         }


    isodt = datetime.now().replace(microsecond=0).isoformat() + '+00:00'
    d = {'last_edited': isodt,
         'last_editor': 'user', 
         'meta': {},
         'locked': False,
         'channels': {'001': ch},
        }
    s = json.dumps(d)
    s = 'config_io=' + s
    print(s)


    token = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    #headers = {'X-Exosite-CIK': token, 'charset': 'utf-8', 'Content-Type': 'application/x-www-form-urlencoded'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    print(headers)

    response = requests.post(url, headers=headers, data=s)

    print(response)
    print(response.headers)
    print(response.text)



def post_data_in():

    d = {'001': random.randint(20, 30)}
    s = json.dumps(d)
    s = 'data_in=' + s
    print(s)

    token = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    #print(headers)

    response = requests.post(url, headers=headers, data=s)

    print(response)
    #print(response.headers)
    print(response.text)



def main():
    token = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'

    #postman()
    #activate()
    #post_config_io()
    while True:
        post_data_in()
        time.sleep(3)

if __name__ == '__main__':
    main()
