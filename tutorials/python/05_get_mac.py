#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from uuid import getnode


if __name__ == "__main__":

    # hardware, mac address
    mac = hex(getnode())
    print('mac: {}'.format(mac))

'''
pi@raspberrypi:~/demo/python/lessons $ python3 05_get_mac.py 
mac: 0xb827eb2bdf76
'''
