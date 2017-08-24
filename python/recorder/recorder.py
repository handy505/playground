#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import threading
import collections


class UidDatabase(object):
    def __init__(self, filepath):
        self.data= collections.OrderedDict()
        self.read_from(filepath)
        keylist = list(self.data.keys())
        self.processing_key = int(keylist[0])
        self.incomming_key = int(keylist[-1])
        self.changed = False


    def append_record(self, rec):
        value = rec.strip('\n')
        key = int(value.split(',')[0])
        self.data[key] = value 
        self.incomming_key = key
        self.changed = True


    def get_record_step_ahead(self):
        keylist = list(self.data.keys()) 
        if self.processing_key in keylist:
            rec = self.data.get(self.processing_key)
            self.processing_key += 1
            return rec
        else:
            return None  
        

    def delete_record(self, uuid):
        keylist = list(self.data.keys()) 
        if uuid in keylist:
            del self.data[uuid]
            self.changed = True
            

    def read_from(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as fr:
            for line in fr.readlines():
                value = line.strip('\n')
                key = int(value.split(',')[0])
                self.data[key] = value
        self.sync_time = time.time()
        self.changed = False


    def write_to(self, filepath):
        lines = []
        for r in list(self.data.values()):
            lines.append('{}\n'.format(r))
        with open(filepath, 'w', encoding='utf-8') as fw:
            fw.writelines(lines)
        self.sync_time = time.time()
        self.changed = False


