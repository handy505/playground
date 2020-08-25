#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime
import serial

import crc
import memorymapping
import concatenate
import devices


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.boards= []
        for id in range(1, 8):
            board= devices.PDUBoard(id)
            print(board)
            self.boards.append(board)
            
        self.concatthread = concatenate.ConcatThread(self.boards, None, None)


    def run(self):
        refresh_timestamp = time.time()
        self.concatthread.start()
        while True:
            now = time.time()
            if now - refresh_timestamp > 3:

                [board.refresh() for board in self.boards]
                [print(board) for board in self.boards]


                #dt = datetime.datetime.fromtimestamp(now)
                #print('Refresh at {}'.format(dt))
                refresh_timestamp = now


def main():
    print('PDU slave simulator')
    mainthread = MainThread()
    mainthread.start()


if __name__ == '__main__':

    main()
