#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import queue
import random
import threading
from datetime import datetime
from collections import namedtuple

class GetIVCurveCommand(object):
    def execute(self):
        print('get ivcurve ')
        time.sleep(1)


class GetInvFirmwareVersion(object):
    def execute(self):
        print('get firmware version')
        time.sleep(1)


def main():
    commands = []
    c = GetIVCurveCommand()
    commands.append(c)

    c = GetInvFirmwareVersion()
    commands.append(c)


    for c in commands:
        c.execute()

if __name__ == '__main__':
    main()
