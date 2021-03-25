#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading
import collections
import json
import re
from uuid import getnode
from urllib import request
import requests
import random


now = lambda: time.strftime('%H:%M:%S', time.localtime(round(time.time())))


class UploadTask(threading.Thread):
    '''
    1) Get record from input pipeline
    2) Make as JSON packet
    3) Upload to server by http post
    4) Response to output pipeline
    5) 3 record formats: event/minute/hour
    '''
    
    def __init__(self,
        eipp=None, mipp=None, hipp=None,
        eopp=None, mopp=None, hopp=None,
        sipp=None):

        threading.Thread.__init__(self)
        self.name = 'upload'
        self.psid = 0

        self.event_post_response = ""
        self.minute_post_response = ""
        self.hour_post_response = ""

        # Queue
        self.event_input_pipeline = eipp
        self.minute_input_pipeline = mipp
        self.hour_input_pipeline = hipp
                
        self.event_output_pipeline = eopp
        self.minute_output_pipeline = mopp
        self.hour_output_pipeline = hopp

        self.status_input_pipeline = sipp
        self.looping = True
        self.observers = []
        self.status = 'init'
        print('[u] {ts} init'.format(ts=now()))


    # observer pattern
    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self):
        [e.update(self) for i, e in enumerate(self.observers)]
            

    def run(self):
        time.sleep(60)
        while self.looping: 
            try:
                self._run2()
            except Exception as ex:
                print(ex)
                self.notify()
                
            time.sleep(10)


    def _run2(self):        
        
        print("[u] {ts} run".format(ts=now()))

        self.status = 'get psid'
        self.notify()
        while self.psid == 0:
            # 透過mac取psid
            mac = "5cf9dd48e7ef"
            url = "http://59.127.196.135/DataStorage/Info.ashx?mac={mac}".format(mac=mac)
            #r = request.urlopen("http://59.127.196.135/DataStorage/Info.ashx?mac=5cf9dd48e7ef")
            r = request.urlopen(url)
            recv_str = r.read().decode("utf-8").split(",") # byte 轉 str 再分割
            self.psid = recv_str[0]
            print("[u] {ts} get psid={psid} by mac={mac}".format(
                ts=time.strftime('%H:%M:%S', time.localtime(time.time())),
                psid=self.psid, 
                mac=mac))

        while self.looping:            
            
            # STATUS uploading
            #self.status = 'STATUS uploading'
            #self.notify()
            if not self.status_input_pipeline.empty(): 
                rec = self.status_input_pipeline.get()
                fields = rec.split(',')      

                # json
                d = collections.OrderedDict()
                d["UniqueID"] = fields[0]
                d["LogTime"] = fields[1]
                d["Normal"] = fields[2]
                d["Alart"] = fields[3]
                d["Error"] = fields[4]
                d["Offline"] = fields[5]
                jsonstr = json.dumps(d)
                poststr = "StatusData@[{}]".format(jsonstr)

                # post
                url = "http://59.127.196.135/DataStorage/DataStorage.ashx?psid=" + self.psid
                r = requests.post(url, data=poststr)

                # real time uploading, needless feedback log process.
                #print(poststr)
                #print(r.text)

            # EVENT uploading
            #self.status = 'EVENT uploading'
            #self.notify()
            while not self.event_input_pipeline.empty():
                rec = self.event_input_pipeline.get()
                pattern = "\d+,\d+,\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+,\d+,[HR],\d+"
                if not re.match(pattern, rec):
                    print("not match: {}".format(rec))
                    break
                fields = rec.split(",")

                # json
                d = collections.OrderedDict()
                d["UniqueID"] = fields[0]
                d["DeviceID"] = fields[1]
                d["LogTime"] = fields[2]
                d["EventType"] = fields[3]
                d["EventIndex"] = fields[4]
                d["EventParameter"] = fields[5]
                d["InverterGood"] = fields[6]
                jsonstr = json.dumps(d)
                poststr = "EventData@[{}]".format(jsonstr)

                # post
                #time.sleep(random.randint(20,200)/1000)
                url = "http://59.127.196.135/DataStorage/DataStorage.ashx?psid=" + self.psid
                r = requests.post(url, data=poststr)

                if len(r.text) < 50:
                    self.event_post_response = r.text
                    
                    recv_str = r.text.split(",")
                    if recv_str[0] == fields[0]:
                        uid = int(fields[0])
                        self.event_output_pipeline.put(uid)
                    self.notify()
                else:
                    print('[u] {ts} server busy ?'.format(ts=now()))

            # MINUTE uploading
            #self.status = 'MINUTE uploading'
            #self.notify()
            while not self.minute_input_pipeline.empty():
                rec = self.minute_input_pipeline.get()

                pattern = "\d+,\d+,\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+"
                if not re.match(pattern, rec):
                    print("not match: {}".format(rec))
                    break
                fields = rec.split(",")
                
                # json
                d = collections.OrderedDict()
                d["UniqueID"] = fields[0]
                d["InverterID"] = fields[1]
                d["Expr1002"] = fields[2]
                d["OutputPower"] = fields[3]
                d["ACVolPhaseA"] = fields[4]
                d["ACVolPhaseB"] = fields[5]
                d["ACVolPhaseC"] = fields[6]
                d["ACFrequency"] = fields[7]
                d["ACOutputCurrentA"] = fields[8]
                d["ACOutputCurrentB"] = fields[9]
                d["ACOutputCurrentC"] = fields[10]
                d["DC1InputVol"] = fields[11]
                d["DC2InputVol"] = fields[12]
                d["DC1InputCurrent"] = fields[13]
                d["DC2InputCurrent"] = fields[14]
                d["DCBusPositiveVol"] = fields[15]
                d["DCBusNegativeVol"] = fields[16]
                d["InternalTemper"] = fields[17]
                d["HeatSinkTemper"] = fields[18]
                d["InputPowerA"] = fields[19]
                d["InputPowerB"] = fields[20]
                d["TotalOutputPower"] = fields[21]
                jsonstr = json.dumps(d)
                poststr = "InverterData@[{}]".format(jsonstr)

                # post
                #time.sleep(random.randint(20,200)/1000)
                url = "http://59.127.196.135/DataStorage/DataStorage.ashx?psid=" + self.psid
                r = requests.post(url, data=poststr)

                if len(r.text) < 50:
                    self.minute_post_response = r.text
                    
                    recv_str = r.text.split(",")
                    if recv_str[0] == fields[0]:
                        uid = int(fields[0])
                        self.minute_output_pipeline.put(uid)
                    self.notify()
                else:
                    print('[u] {ts} server busy ?'.format(ts=now()))

            # HOUR uploading
            #self.status = 'HOUR uploading'
            #self.notify()
            while not self.hour_input_pipeline.empty():
                rec = self.hour_input_pipeline.get()
                pattern = "\d+,\d+,\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+"
                if not re.match(pattern, rec):
                    print("not match: {}".format(rec))
                    break
                fields = rec.split(",")
                
                # json
                d = collections.OrderedDict()
                d["UniqueID"] = fields[0]
                d["InverterID"] = fields[1]
                d["Expr1002"] = fields[2]
                d["OutputPower"] = fields[3]
                d["ACVolPhaseA"] = fields[4]
                d["ACVolPhaseB"] = fields[5]
                d["ACVolPhaseC"] = fields[6]
                d["ACFrequency"] = fields[7]
                d["ACOutputCurrentA"] = fields[8]
                d["ACOutputCurrentB"] = fields[9]
                d["ACOutputCurrentC"] = fields[10]
                d["DC1InputVol"] = fields[11]
                d["DC2InputVol"] = fields[12]
                d["DC1InputCurrent"] = fields[13]
                d["DC2InputCurrent"] = fields[14]
                d["DCBusPositiveVol"] = fields[15]
                d["DCBusNegativeVol"] = fields[16]
                d["InternalTemper"] = fields[17]
                d["HeatSinkTemper"] = fields[18]
                d["InputPowerA"] = fields[19]
                d["InputPowerB"] = fields[20]
                d["TotalOutputPower"] = fields[21] 
                d["PrevTotalOutputPower"] = fields[22] # 2017 new add
                d["DiffTotalOutputPower"] = fields[23] # 2017 new add
                jsonstr = json.dumps(d)
                poststr = "InverterDataH@[{}]".format(jsonstr)

                # post
                #time.sleep(random.randint(20,200)/1000)
                url = "http://59.127.196.135/DataStorage/DataStorage.ashx?psid=" + self.psid
                r = requests.post(url, data=poststr)

                if len(r.text) < 50:
                    self.hour_post_response = r.text
                    
                    recv_str = r.text.split(",")
                    if recv_str[0] == fields[0]:
                        uid = int(fields[0])
                        self.hour_output_pipeline.put(uid)
                        s = '[u] {ts} uploaded hour record {uploaded_id}'.format(
                            ts=time.strftime('%H:%M:%S', time.localtime(time.time())),
                            uploaded_id=uid)
                        print(s)
                    self.notify()
                else:
                    print('[u] {ts} server busy ?'.format(ts=now()))
    

            time.sleep(1)

        self.status = 'end'
        self.notify()
        print('[u] {ts} end'.format(ts=now()))


if __name__ == "__main__":
    # python3 -m doctest filename.py -v
    import doctest
    doctest.testmod()
