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
    start = time.time()
    while True:
        do_job()

