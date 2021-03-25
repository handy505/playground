#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()


    def run(self):
        print('hello simple solarpi')


def main():
    mainthread = MainThread()
    mainthread.start()


if __name__ == '__main__':
    main()
