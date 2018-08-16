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
        
        self.event_rows = []
        self.measurement_rows = []
        self.hourly_measurement_rows = []
        self.illu_rows = []
        self.illuhour_rows = []
        self.temp_rows = []
        self.temphour_rows = []

        minutely_datetime = datetime.datetime.now()
        while True:
            try:
                self.uploading_events()
                self.uploading_measurements()
                self.uploading_hourly_measurements()
                self.uploading_illu()
                self.uploading_illuhour()
                self.uploading_temp()
                self.uploading_temphour()

                if datetime.datetime.now().minute != minutely_datetime.minute:
                    self.uploading_status()
                    minutely_datetime = datetime.datetime.now()

            except requests.exceptions.ConnectionError as ex:
                print('exception: {}'.format(repr(ex)))

            time.sleep(1)


    def uploading_illu(self):
        if not self.illu_rows:
            while not self.ibus.illu.empty():
                row = self.ibus.illu.get()
                self.illu_rows.append(row)

        if self.illu_rows:
            jsonstr = self.make_illu_jsonstr(self.illu_rows)
            poststr = 'IlluminationData@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('uploaded illu: {}'.format(ruid))
            expect_ruid = self.illu_rows[-1].uid
            if int(ruid) == expect_ruid:
                self.obus.illu.put(ruid)
                self.illu_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()
        

    def uploading_illuhour(self):
        if not self.illuhour_rows:
            while not self.ibus.illuhour.empty():
                row = self.ibus.illuhour.get()
                self.illuhour_rows.append(row)

        if self.illuhour_rows:
            jsonstr = self.make_illuhour_jsonstr(self.illuhour_rows)
            poststr = 'IlluminationDataH@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('uploaded illuhour: {}'.format(ruid))
            expect_ruid = self.illuhour_rows[-1].uid
            if int(ruid) == expect_ruid:
                self.obus.illuhour.put(ruid)
                self.illuhour_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_temp(self):
        if not self.temp_rows:
            while not self.ibus.temp.empty():
                row = self.ibus.temp.get()
                self.temp_rows.append(row)

        if self.temp_rows:
            jsonstr = self.make_illu_jsonstr(self.temp_rows)
            poststr = 'TemperatureData@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('uploaded temp: {}'.format(ruid))
            expect_ruid = self.temp_rows[-1].uid
            if int(ruid) == expect_ruid:
                self.obus.temp.put(ruid)
                self.temp_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()
        

    def uploading_temphour(self):
        if not self.temphour_rows:
            while not self.ibus.temphour.empty():
                row = self.ibus.temphour.get()
                self.temphour_rows.append(row)

        if self.temphour_rows:
            jsonstr = self.make_illuhour_jsonstr(self.temphour_rows)
            poststr = 'TemperatureDataH@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            print('uploaded temphour: {}'.format(ruid))
            expect_ruid = self.temphour_rows[-1].uid
            if int(ruid) == expect_ruid:
                self.obus.temphour.put(ruid)
                self.temphour_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()







    def uploading_hourly_measurements(self):
        if not self.hourly_measurement_rows:
            while not self.ibus.measurehour.empty():
                row = self.ibus.measurehour.get()
                self.hourly_measurement_rows.append(row)

        if self.hourly_measurement_rows:
            jsonstr = self.make_hour_jsonstr(self.hourly_measurement_rows)
            poststr = 'InverterDataH@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            #print('hourly measurement resp: {}'.format(ruid))
            print('uploaded hourly measurement: {}'.format(ruid))
            expect_ruid = self.hourly_measurement_rows[-1].uid
            #print('expect ruid: {}'.format(expect_ruid))
            if int(ruid) == expect_ruid:
                self.obus.measurehour.put(ruid)
                self.hourly_measurement_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_measurements(self):
        if not self.measurement_rows:
            while not self.ibus.measure.empty():
                row = self.ibus.measure.get()
                self.measurement_rows.append(row)


        if self.measurement_rows:
            jsonstr = self.make_minute_jsonstr(self.measurement_rows)
            poststr = 'InverterData@{}'.format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            #print('measurement resp: {}'.format(ruid))
            print('uploaded measurement: {}'.format(ruid))
            expect_ruid = self.measurement_rows[-1].uid
            if int(ruid) == expect_ruid:
                self.obus.measure.put(ruid)
                self.measurement_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_events(self):
        if not self.event_rows:
            while not self.ibus.event.empty():
                row = self.ibus.event.get()
                self.event_rows.append(row)

        if self.event_rows:
            jsonstr = self.make_event_jsonstr(self.event_rows)
            poststr = "EventData@{}".format(jsonstr)
            resp = requests.post(self.target_url, data=poststr)
            (ruid, ms) = resp.text.split(',')
            #print('event resp: {}'.format(ruid))
            print('uploaded event: {}'.format(ruid))
            expect_ruid = self.event_rows[-1].uid
            if int(ruid) == expect_ruid:
                self.obus.event.put(ruid)
                self.event_rows.clear()
            else:
                print('Uploading fail, how to do this ???')
                sys.exit()


    def uploading_status(self):
        jsonstr = self.make_status_jsonstr()
        poststr = 'StatusData@[{}]'.format(jsonstr)
        resp = requests.post(self.target_url, data=poststr)
        (ruid, ms) = resp.text.split(',')
        #print('status resp: {}, {}'.format(ruid, ms))
        print('uploaded status: {}, {}'.format(ruid, ms))



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

    def make_illu_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["DeviceID"] = row.mid
            d["LogTime"] = row.timestring
            d["Illumination"] = row.value
            records.append(d)
        result = json.dumps(records)
        return result


    def make_illuhour_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["DeviceID"] = row.mid
            d["LogTime"] = row.timestring
            d["Illumination"] = row.value
            records.append(d)
        result = json.dumps(records)
        return result


    def make_temp_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["DeviceID"] = row.mid
            d["LogTime"] = row.timestring
            d["Temperature"] = row.value
            records.append(d)
        result = json.dumps(records)
        return result


    def make_temphour_jsonstr(self, rows):
        records = []
        for row in rows:
            d = collections.OrderedDict()
            d["UniqueID"] = row.uid
            d["DeviceID"] = row.mid
            d["LogTime"] = row.timestring
            d["Temperature"] = row.value
            records.append(d)
        result = json.dumps(records)
        return result



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




