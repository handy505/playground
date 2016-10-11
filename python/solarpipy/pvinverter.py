#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    強化後的PVInverter
    1) 基本對映到485彼端的實體機器參數(V/I/P)
    2) 有alarm/event佇列
    3) 每小時平均
    4) 寫時間到機器(村哥)
    5) serial_task的jbus行為也包成機器行為
"""
class PVInverter(object):
    """ doctest here
    >>> pv = PVInverter()
    >>> pv.id
    1
    >>> pv.id = 2
    >>> pv.id
    2
    """
    def __init__(self):
        self._id = 1
        self._type = "pv"
        self._tmp = 0
        self._volt = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, arg):
        self._id = arg

    @property
    def volt(self):
        return self._volt

    
    def simu_generate(self):
        self._tmp += 1
        self._volt = self._tmp

if __name__ == "__main__":
    # python3 -m doctest filename.py -v
    import doctest
    doctest.testmod()
    