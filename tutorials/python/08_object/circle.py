#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import math


class Circle(object):
    def __init__(self, x=0, y=0, radius=1):
        self.x = x
        self.y = y
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def perimeter(self):
        return 2 * self.radius * math.pi


if __name__ == "__main__":
    c = Circle()
    print(c.area())
    print(c.perimeter())

    c = Circle(1,2,3)
    print(c.area())
    print(c.perimeter())

'''
3.141592653589793
6.283185307179586
28.274333882308138
18.84955592153876
'''
