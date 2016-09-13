#!/usr/bin/env python3
import os
import time


LOGFILE = "temp.log"

def get_last_record(filename):

    last_record = ""
    try:
        # check file is exist
        if os.path.exists(LOGFILE):
            #print("exist")
            with open(filename, "r") as f:
                for line in f:
	                #print("line: " + line, end="")
                    #print("line: " + line)
                    if line != "\n":
                        last_record = line.rstrip("\n")
                #print("lr: " + last_record)
            return last_record
        else:
            print("file not exist, create it.")
            with open(LOGFILE, "w") as f:
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(round(time.time())))
                temp = os.popen("vcgencmd measure_temp").read()
                f.write("{}, {}\n".format(ts, temp))
                exit()
    except ValueError:
        print(ValueError)
        exit()

currentTemp = os.popen("vcgencmd measure_temp").read()
print(currentTemp)

lastRecord = get_last_record(LOGFILE)
#print("last record: " + lastRecord)

elem = lastRecord.split(",")
#print("elem: " + str(elem))

maxtemp = elem[1].lstrip(" ")
#print(temp)
#print(maxtemp)

ftnow = float(currentTemp[5:9])
ftmax = float(maxtemp[5:9])
if ftnow > ftmax:
        with open(LOGFILE, "w") as f:
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(round(time.time())))
                max_temp_string = "{}, {}\n".format(ts, currentTemp)
                f.write(max_temp_string)
                print("update temp log... {}".format(max_temp_string), end="")

