#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import time


class ATask(threading.Thread):

    def __init__(self, condition1, condition2, packet1, packet2):
        threading.Thread.__init__(self)
        self.c1 = condition1
        #self.c2 = condition2
        self.packet1 = packet1
        #self.packet2 = packet2

    def run(self):
        
        while True:
            ip = input()

            self.c1.acquire()

            ts = time.strftime('%H:%M:%S', time.localtime(round(time.time())))
            tstr = "[a] {}, {}".format(ts, ip)
            self.packet1 = tstr
            print(self.packet1)

            self.c1.notify_all()

            self.c1.release()


            time.sleep(1)


class BTask(threading.Thread):

    def __init__(self, condition1, condition2, packet1, packet2):
        threading.Thread.__init__(self)
        self.c1 = condition1
        #self.c2 = condition2
        self.packet1 = packet1
        #self.packet2 = packet2

    def run(self):
        
        while True:
            ts = time.strftime('%H:%M:%S', time.localtime(round(time.time())))
            print("[b] {}".format(ts))
            
            self.c1.acquire()

        
            self.c1.wait(3)
            print(self.packet1) #需修與字串參考指向不同實體的問題，才能做到thread同步
            if self.packet1:
                print("[b] processing...{}".format(self.packet1))
                time.sleep(1)        
                self.packet1 = ""
                
            

            self.c1.release()


            #time.sleep(5)



if __name__ == "__main__":

    lock1 = threading.Lock()
    lock2 = threading.Lock()
    condition1 = threading.Condition()
    condition2 = threading.Condition()

    packet1 = "iampacket1111"
    packet2 = "2222222222222"

    tha = ATask(condition1, condition2, packet1, packet2)
    tha.start()

    thb = BTask(condition1, condition2, packet1, packet2)
    thb.start()