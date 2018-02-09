#! /bin/env python3
# -*- coding:utf-8 -*-

from sympy import *
import math


TARGET_TEMP = 70
TARGET_VOLUMN = 30
HOT_TEMP = 100
COLD_TEMP = 25


def main():
  
    # hot_volumn + cold_volumn = target_volumn
    # abs(target_tem - hot_temp)*hot_volumn = abs(target_temp - cold_temp)*cold_volumn
    """
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    f1 = 4*x + 3*y + 3*z - 350
    f2 = 4*x + 2*y + 5*z - 360
    f3 = 8*x + 8*y + 10*z - 840

    sol = solve((f1, f2, f3), x, y, z)
    pprint(sol)
    """

    x = Symbol('x')
    y = Symbol('y')

    #f1 = (100-70)*x - (70-25)*y 
    #f2 = x + y - 60 

    f1 = (HOT_TEMP-TARGET_TEMP)*x - (TARGET_TEMP-COLD_TEMP)*y 
    f2 = x + y - TARGET_VOLUMN 

    sol = solve((f1, f2), x, y)
    pprint(sol)
 

if __name__ == "__main__":
    main()
