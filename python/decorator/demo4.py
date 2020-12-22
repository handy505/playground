#!/usr/bin/env python3
import functools


def unit(multiple):

    def wrapper2(fn):
        @functools.wraps(fn)
        def wrapper():
            return fn() * multiple 
        return wrapper 

    return wrapper2


@unit(0.1)
def getvalue():
    return 100


if __name__ == '__main__':
    print(getvalue())
    print(getvalue.__name__)

'''
$ python3 demo4.py
10.0
getvalue

'''
