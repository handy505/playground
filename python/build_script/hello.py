#!/usr/bin/env python3

import myobj

if __name__ == '__main__':

    print('hello build')
    c = myobj.Circle()
    c.radius = 3
    print(c.area)