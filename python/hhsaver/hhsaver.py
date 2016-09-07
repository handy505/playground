#!/usr/bin/env python3
# Half-Hour Saver, save your annual leave

import time
import os
import os.path
import math
import gui

def get_last_record(filename):

    last_record = ""

    # check file is exist
    if os.path.exists("/home/handy/democode/python/hhsaver/arrived.log"):
        #print("exist")
        with open(filename, "r") as f:
            for line in f:
                #print(line, end="")
                last_record = line.rstrip("\n")        
    else:
        print("file not exist, create it.")
        with open("arrived.log", "w") as f:
            rec = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(round(time.time())))
            f.write(rec + "\n")
            last_record = rec

    return last_record


def odd_hms(seconds):
    hour = int(seconds//(60*60))
    min = int((seconds%(60*60)) // 60)
    sec = int((seconds%(60*60)) % 60)
    return hour, min, sec


if __name__ == '__main__':

    wlan0_get_ip = os.popen('/sbin/ifconfig | /bin/grep "inet addr"').read()
    if wlan0_get_ip != "":

        # current timestamp
        t1 = round(time.time())
        lc1 = time.localtime(t1)

        # last record timestamp
        try:
            last_record = get_last_record("arrived.log")
            lc2 = time.strptime(last_record, '%Y-%m-%d %H:%M:%S')
            print("ts2-arrived: " + time.strftime('%Y-%m-%d %H:%M:%S', lc2) )            
        except ValueError:
            print(ValueError)
            exit()

        
        the_same_day = ((lc1.tm_year == lc2.tm_year) and (lc1.tm_mon == lc2.tm_mon) and (lc1.tm_mday == lc2.tm_mday)) 
        if not the_same_day:
            print("a new day")
            with open("arrived.log", "a") as f:
                f.write( time.strftime('%Y-%m-%d %H:%M:%S', lc1) + "\n")

        # calculate timestamp
        t2 = time.mktime(lc2)
        t3 = t2 + (60*60*9)
        lc3 = time.localtime(t3)
        print("ts3-freedom: " + time.strftime('%Y-%m-%d %H:%M:%S', lc3) )
        print("ts1-current: " + time.strftime('%Y-%m-%d %H:%M:%S', lc1) )

        hour, min, sec = odd_hms(t3-t1)
        print("get off work: {}:{}:{}".format(hour, min, sec))

        if t1 > t3:
            gui.mainview()

    else: 
        print('not arrived')


