#!/usr/bin/env python3
import functools

def f1(f):
    @functools.wraps(f)
    def wrap():
        print('aaa')
        f()
        print('bbb')
    return wrap 
    
@f1
def f2():
    print('222')


#x = f1(f2)
#f2()
#print(f2.__name__)



'''def unit(multiple=0.1):
    def unitadj(fn):
        @functools.wraps(fn)
        def wrap():
            return fn() * multiple
        return wrap
    return unitadj
'''

def unit(multiple=0.1):
    def decorator(fn):
        @functools.wraps(fn)
        def wrap():
            return fn() * multiple
        return wrap
    return decorator

@unit(0.1)
def getvalue():
    return 100



print(getvalue())
