#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import random
from datetime import datetime

import exosense
from ablerex import AblerexInverterSimulator
from meter import IlluMeterSimulator, TempMeterSimulator


def activate():
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/provision/activate'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8' }
    data = 'id=Ablerex_010'
    response = requests.post(url, headers=headers, data=data)
    print(data)
    print(response)
    print(response.text)


def post_config_io(token):
    d = exosense.create_inverter_config_io()
    s = json.dumps(d)
    s = 'config_io=' + s
    print(s)

    #token = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    print(headers)

    response = requests.post(url, headers=headers, data=s)

    print(response)
    print(response.headers)
    print(response.text)


def post_data_in():
    d = {'DC1Voltage': random.randint(500, 1000),
         'DC2Voltage': random.randint(500, 1000),
         'DC3Voltage': random.randint(500, 1000),
         'DC4Voltage': random.randint(500, 1000),
         'DC1Current': random.randint(0, 10),
         'DC2Current': random.randint(0, 10),
         'DC3Current': random.randint(0, 10),
         'DC4Current': random.randint(0, 10),
         'DC1Power'  : random.uniform(0, 100),
         'DC2Power'  : random.uniform(0, 100),
         'DC3Power'  : random.uniform(0, 100),
         'DC4Power'  : random.uniform(0, 100),

         'DCPositive'  : random.uniform(0, 100),
         'DCNegative'  : random.uniform(0, 100),
         'InternalTemp': random.uniform(0, 100),
         'HeatSinkTemp': random.uniform(0, 100),

         'AC1Voltage': random.uniform(0, 100),
         'AC2Voltage': random.uniform(0, 100),
         'AC3Voltage': random.uniform(0, 100),
         'AC1Current': random.uniform(0, 100),
         'AC2Current': random.uniform(0, 100),
         'AC3Current': random.uniform(0, 100),

         'ACFrequency'  : random.uniform(0, 100),
         'ACOutputPower': random.uniform(0, 100),
         'KWH'          : random.uniform(0, 100),
        }
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



def simulator():
    inverters = [AblerexInverterSimulator(id) for id in range(1,7+1)]
    print(inverters)
    meters = [IlluMeterSimulator(248), TempMeterSimulator(249)]
    print(meters)

    while True:
        for inv in inverters:
            inv.sync_with_hardware()
            rec = inv.create_record()
            print(rec)

        for m in meters:
            m.sync_with_hardware()
            rec = m.create_record()
            print(rec)

        time.sleep(2)


token1 = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
token2 = '3OkFwBFRDYuvfcFunfNJKAjTDNWS4sAOEpRJCoee'
token3 = '7rHUQiXsciKCZ93jdf3GsreKSnfdxLKVwY4ZfC9X'
token4 = 'ALJHgNxkyNf7FXGvyaPTmoDE2YoWFgvtfvjTRkXp'
token5 = 'bp5dZgS0ms1VA002qL24NiR7V9MIolIenMsz58c9'
token6 = 'nVVY8yGCWFTsMaVH82L5nh4kc8IWePplKAShuIbK'
token7 = 'ZGnRLjst9qdgu7xUti8DMLmh58B4mFINOsKGHvPs'
token8 = 'LDXIwnEebOXZxnL7hpFV1Fr3Jf9ATw42DK5YpQjP'
token9 = '2OIKqs26lXkSUlPvs2B9J2ZYak2PNAmygaCvUAB8'
token10 = '2OIKqs26lXkSUlPvs2B9J2ZYak2PNAmygaCvUAB8'

token_dict = {'Ablerex_001': token1,
              'Ablerex_002': token2,
              'Ablerex_003': token3,
              'Ablerex_004': token4,
              'Ablerex_005': token5,
              'Ablerex_006': token6,
              'Ablerex_007': token7,
              'Ablerex_008': token8,
              'Ablerex_009': token9,
              'Ablerex_010': token10,
             }

device_name_dict = {1:  'Ablerex_001',
                    2:  'Ablerex_002',
                    3:  'Ablerex_003',
                    4:  'Ablerex_004',
                    5:  'Ablerex_005',
                    6:  'Ablerex_006',
                    7:  'Ablerex_007',
                    8:  'Ablerex_008',
                    9:  'Ablerex_009',
                    10: 'Ablerex_010',
                   }

def get_token(id):
    device_name = device_name_dict.get(id)
    return token_dict.get(device_name)

def creatre_meter_record_dict(rec):
    d = {'Value': rec.Value}
    return d

def create_gateway_record_dict():
    d = {'MAC': 'B827EBB62B45',
         'ServiceID': '781924159'
        }
    return d


def create_inverter_record_dict(rec):
    d = {'DC1Voltage': rec.DC1Voltage,
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


def post_to_exosence(d, token):
    s = json.dumps(d)
    s = 'data_in=' + s
    #print(s)

    url = 'https://m21d2g4j50cu80000.m2.exosite.io/onep:v1/stack/alias'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8',
               'X-Exosite-CIK': token}
    response = requests.post(url, headers=headers, data=s)
    print(response)



if __name__ == '__main__':
    '''for i in range(1,6+1):
        d = exosense.create_inverter_config_io()
        t = get_token(i)
        exosense.post_config_io(d, t)

    d = exosense.create_meter_config_io()
    t = get_token(7)
    exosense.post_config_io(d, t)

    d = exosense.create_meter_config_io()
    t = get_token(8)
    exosense.post_config_io(d, t)

    d = exosense.create_gateway_config_io()
    t = get_token(9)
    exosense.post_config_io(d, t)
    sys.exit()
    '''


    d = create_gateway_record_dict()
    token = get_token(9)
    post_to_exosence(d, token)



    inverters = [AblerexInverterSimulator(id) for id in range(1,6+1)]
    print(inverters)
    meters = [IlluMeterSimulator(8), TempMeterSimulator(9)]
    print(meters)

    while True:
        for inv in inverters:
            print(inv.id)
            inv.sync_with_hardware()
            rec = inv.create_record()

            d = create_inverter_record_dict(rec)
            token = get_token(rec.ID)
            post_to_exosence(d, token)


        for m in meters:
            print(m.id)
            m.sync_with_hardware()
            rec = m.create_record()

            d = creatre_meter_record_dict(rec)
            print(d)
            token = get_token(rec.ID)
            post_to_exosence(d, token)



        time.sleep(2)



