#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from uuid import getnode


if __name__ == "__main__":

    # hardware, mac address
    mac = getnode()
    mac = hex(mac)

    mac = hex(getnode())
    print('mac: {}'.format(mac))


'''
mac: 0x1ede57df52d
'''
