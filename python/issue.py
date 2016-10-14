#!/usr/bin/env python3

class Car(object):
    def __init__(self):
        self._alarm = [False for _ in range(0, 8)]
        self._alarm2 = self._alarm

    @property
    def alarm(self):
        return self._alarm

    @alarm.setter
    def alarm(self, arg):
        print("1: {}".format(self._alarm))
        self._alarm2 = self._alarm
        print("2: {}".format(self._alarm))
        self._alarm = arg
        print("3: {}".format(self._alarm))


if __name__ == "__main__":

    print("hello car")
    c = Car()

    seq = [False for _ in range(0,8)]
    c.alarm = seq
    seq[1] = True
    c.alarm = seq
'''
handy@handy-dell ~/tmp $ python3 issue.py 
hello car
1: [False, False, False, False, False, False, False, False]
2: [False, False, False, False, False, False, False, False]
3: [False, False, False, False, False, False, False, False]
1: [False, True, False, False, False, False, False, False]
2: [False, True, False, False, False, False, False, False]
3: [False, True, False, False, False, False, False, False]

'''
