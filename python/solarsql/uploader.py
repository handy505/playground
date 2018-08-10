#!/usr/bin/env python3
import threading
import time
import queue
import sys
import os
import requests
import json
import collections
import datetime

import recorderdb
import event


def get_psid():
    cmd = "hciconfig | grep Address | awk {'print $3'}"
    mac = os.popen(cmd).read().strip('\n')
    mac = mac.replace(':', '')
    url = "http://59.127.196.135/DataStorage/Info.ashx?mac={}".format(mac)
    r = requests.get(url)
    fields = r.text.split(',')
    if fields[0].isdigit():
        psid = fields[0] 
    return psid


class Uploader(threading.Thread):
    def __init__(self, ibus, obus):
        threading.Thread.__init__(self)       
        self.ibus = ibus 
        self.obus = obus 


    def run(self):
        psid = get_psid()
        print('psid: {}'.format(psid))
        self.target_url = 'http://59.127.196.135/DataStorage/DataStorage.ashx?psid={}'.format(psid)

        
        minutely_datetime = datetime.datetime.now()

        while True:
            self.uploading_events()
            self.uploading_measurements()
            self.uploading_hourly_measurements()


            if datetime.datetime.now().minute != minutely_datetime.minute:
                self.uploading_status()
                minutely_datetime = datetime.datetime.now()

            time.sleep(1)


    def uploading_hourly_measurements(self):
        rows = []
        while not self.ibus.measurehour.empty():
            row = self.ibus.measurehour.get()
            rows.append(row)

        if rows:
            jsonstr = self.make_hour_jsonstr(rows)
            poststr = 'InverterDataH@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('hourly measurement resp: {}'.format(ruid))
            if ruid:
                self.obus.measurehour.put(ruid)
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_measurements(self):
        rows = []
        while not self.ibus.measure.empty():
            row = self.ibus.measure.get()
            rows.append(row)

        if rows:
            jsonstr = self.make_minute_jsonstr(rows)
            poststr = 'InverterData@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('measurement resp: {}'.format(ruid))
            if ruid:
                self.obus.measure.put(ruid)
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_events(self):
        rows = []
        while not self.ibus.event.empty():
            row = self.ibus.event.get()
            rows.append(row)

        if rows:
            jsonstr = self.make_event_jsonstr(rows)
            poststr = "EventData@{}".format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('event resp: {}'.format(ruid))
            if ruid:
                self.obus.event.put(ruid)
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_status(self):
        jsonstr = self.make_status_jsonstr()
        poststr = 'StatusData@[{}]'.format(jsonstr)
        resp = requests.post(self.target_url, data=poststr)
        (ruid, ms) = resp.text.split(',')
        print('status resp: {}, {}'.format(ruid, ms))




    def make_status_jsonstr(self):
        d = collections.OrderedDict()
        d["UniqueID"] = 99
        timestring = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        d["LogTime"] = timestring
        d["Normal"] = 13
        d["Alart"] = 0
        d["Error"] = 0
        d["Offline"] = 2
        jsonstr = json.dumps(d)
        return jsonstr 


    def make_event_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["DeviceID"] = row.mid
            d["LogTime"] = row.timestring
            d["EventType"] = row.event_type
            d["EventIndex"] = row.event_index
            d["EventParameter"] = row.event_parameter
            d["InverterGood"] = row.inverter_good
            records.append(d)
        result = json.dumps(records)
        return result


    def make_minute_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["InverterID"] = row.mid
            d["Expr1002"] = row.timestring
            d["OutputPower"] = row.OutputPower
            d["ACVolPhaseA"] = row.ACVolPhaseA
            d["ACVolPhaseB"] = row.ACVolPhaseB
            d["ACVolPhaseC"] = row.ACVolPhaseC
            d["ACFrequency"] = row.ACFrequency
            d["ACOutputCurrentA"] = row.ACOutputCurrentA
            d["ACOutputCurrentB"] = row.ACOutputCurrentB
            d["ACOutputCurrentC"] = row.ACOutputCurrentC
            d["DC1InputVol"] = row.DC1InputVol
            d["DC2InputVol"] = row.DC2InputVol
            d["DC1InputCurrent"] = row.DC1InputCurrent
            d["DC2InputCurrent"] = row.DC2InputCurrent
            d["DCBusPositiveVol"] = row.DCBusPositiveVol
            d["DCBusNegativeVol"] = row.DCBusNegativeVol
            d["InternalTemper"] = row.InternalTemper
            d["HeatSinkTemper"] = row.HeatSinkTemper
            d["InputPowerA"] = row.InputPowerA
            d["InputPowerB"] = row.InputPowerB
            d["TotalOutputPower"] = row.TotalOutputPower
            records.append(d)
        result = json.dumps(records)
        return result


    def make_hour_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["InverterID"] = row.mid
            d["Expr1002"] = row.timestring
            d["OutputPower"] = row.OutputPower
            d["ACVolPhaseA"] = row.ACVolPhaseA
            d["ACVolPhaseB"] = row.ACVolPhaseB
            d["ACVolPhaseC"] = row.ACVolPhaseC
            d["ACFrequency"] = row.ACFrequency
            d["ACOutputCurrentA"] = row.ACOutputCurrentA
            d["ACOutputCurrentB"] = row.ACOutputCurrentB
            d["ACOutputCurrentC"] = row.ACOutputCurrentC
            d["DC1InputVol"] = row.DC1InputVol
            d["DC2InputVol"] = row.DC2InputVol
            d["DC1InputCurrent"] = row.DC1InputCurrent
            d["DC2InputCurrent"] = row.DC2InputCurrent
            d["DCBusPositiveVol"] = row.DCBusPositiveVol
            d["DCBusNegativeVol"] = row.DCBusNegativeVol
            d["InternalTemper"] = row.InternalTemper
            d["HeatSinkTemper"] = row.HeatSinkTemper
            d["InputPowerA"] = row.InputPowerA
            d["InputPowerB"] = row.InputPowerB
            d["TotalOutputPower"] = row.TotalOutputPower
            d["PrevTotalOutputPower"] = row.PrevTotalOutputPower
            d["DiffTotalOutputPower"] = row.DiffTotalOutputPower
            records.append(d)
        result = json.dumps(records)
        return result


if __name__ == '__main__':
    print(get_psid())




