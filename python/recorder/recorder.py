#/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import threading
import collections


class LogModle(object):
    ''' Record collections '''

    def __init__(self, filepath):
        self.dc = collections.OrderedDict()
        self.uploading_key = 0
        self.incomming_key = 0


        with open(filepath, "r", encoding="utf-8") as fr:
            for line in fr.readlines():
                line = line.strip("\n")

                fields = line.split(',')
                key = fields[0]
                value = line
                self.dc[key] = value

        for k in self.dc.keys():
            self.uploading_key = k
            break

        for k in self.dc.keys():
            self.incomming_key = k




class Recorder(threading.Thread): 

    def __init__(self, mipp=None, mopp=None, mfpp=None):
        threading.Thread.__init__(self)

        self.name = 'recorder' 
        self.looping = True

        self.minute_input_pipeline = mipp
        self.minute_output_pipeline = mopp
        self.minute_feedback_pipeline = mfpp
        
        self.mm = LogModle()
        self.mm.load(MINUTE_FILEPATH, MINUTE_FILTER_PATTERN)

    def run(self):

        while self.looping:

            # MINUTE database input/output/feedback process
            while not self.minute_input_pipeline.empty():
                s = self.minute_input_pipeline.get()
                self.mm.append(s)

            # output records
            if self.minute_output_pipeline.empty():
                while ( self.mm.ruidx < len(self.mm.rlist) 
                and self.minute_output_pipeline.qsize() < 30):
                    r = self.mm.get_record(self.mm.ruidx)
                    self.minute_output_pipeline.put(r)
                    self.mm.ruidx += 1

            # remove uploaded records from feedback pipeline
            while not self.minute_feedback_pipeline.empty():
                uid = self.minute_feedback_pipeline.get()
                self.mm.remove(uid)

            # synchronize log file
            if (time.time() - self.mm.timestamp > 60
            and self.mm.changed_count > 0):
                self.mm.zip_records()
                self.mm.save(MINUTE_FILEPATH)

            time.sleep(3)
        

