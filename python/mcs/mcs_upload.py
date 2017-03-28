#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen

if __name__ == '__main__':

    url = 'https://api.mediatek.com/mcs/v2/devices/DoDRf1I3/connections.csv'
    
    r = Request(url)
    r.add_header('DeviceKey', 'LThU2YXaK8RETiXd')
    
    recv_str = urlopen(r).read()
    print(recv_str)
