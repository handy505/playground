#!/usr/bin/env python3
import threading
import time
import queue
import sys
import os
import requests
import json
import collections

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

        while True:
            self.event_uploading()
            self.measure_uploading()
            self.measurehour_uploading()
            time.sleep(1)

    def measurehour_uploading(self):
        pass




    def measure_uploading(self):
        try:
            rows = []
            while not self.ibus.measure.empty():
                row = self.ibus.measure.get()
                rows.append(row)

            if rows:
                jsonstr = self.make_minute_jsonstr(rows)
                poststr = 'InverterData@{}'.format(jsonstr)
                resp = requests.post(self.target_url, data=poststr)
                (ruid, ms) = resp.text.split(',')
                print('resp: {}, {}'.format(ruid, ms))
                if ruid:
                    self.obus.measure.put(ruid)
                else:
                    print('Uploading fail, how to do this ???')

                #uids = [row.uid for row in rows]
                #[self.obus.measure.put(uid) for uid in uids]
        except Exception as ex:
            print('Exception in measure_uploading(), {}'.format(repr(ex)))



    def event_uploading(self):
        rows = []
        while not self.ibus.event.empty():
            row = self.ibus.event.get()
            rows.append(row)

        uids = [row.uid for row in rows]
        [self.obus.event.put(uid) for uid in uids]



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


if __name__ == '__main__':
    print(get_psid())




