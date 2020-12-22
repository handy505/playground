#!/usr/bin/env python3
import functools


def f0(func):
    def wrap():
        print('aaa')
        func()
        print('bbb')
    return wrap 


def f1(func):
    @functools.wraps(func)
    def wrap():
        print('aaa')
        func()
        print('bbb')
    return wrap 
    

def f2():
    print('222')


@f1
def f3():
    print('333')


if __name__ == '__main__':

    f = f0(f2)
    f()
    print(f.__name__)
    print('------------------')

    f = f3
    f()
    print(f.__name__)

'''
$ python3 demo2.py 
aaa
222
bbb
wrap
------------------
aaa
333
bbb
f3

'''
