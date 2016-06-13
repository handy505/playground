#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import math


class Circle(object):
    def __init__(self, x=0, y=0, radius=1):
        self.x = x
        self.y = y
        self.__r = radius

    @property
    def radius(self):
        return self.__r

    @radius.setter
    def radius(self, arg):
        self.__r = arg

    @property
    def area(self):
        return math.pi * (self.radius ** 2)

    @property
    def perimeter(self):
        return 2 * self.radius * math.pi

if __name__ == "__main__":
    c = Circle()
    print(c.area)

