#!/usr/bin/env python3
import time
import functools


class EveryXSeconds(object):
    def __init__(self, seconds):
        self.seconds = seconds
        self.last_time = time.time()

    def __call__(self, func):
        def wrapper(*args, **wkargs):
            if time.time() - self.last_time > self.seconds:
                func()
                self.last_time = time.time()
        return wrapper


@EveryXSeconds(3)
def do_job():
    print(time.time())


if __name__ == '__main__':
    while True:
        do_job()

'''
output1: unuse decorator:
1608624805.0863774
1608624805.0864005
1608624805.0864198

-----------------------------
output2: use decorator:
1608624735.2194827
1608624738.2195969
1608624741.2196589

'''
