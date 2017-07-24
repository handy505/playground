#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

import recorder 


class TestRecorder(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_record_modle(self):
        datamodle = recorder.LogModle('./minute.txt')

        rec = datamodle.dc.get('1')
        self.assertEqual('1,2017/01/01 00:00:00,1000', rec)

        self.assertEqual(7, len(datamodle.dc))
        self.assertEqual('1', datamodle.uploading_key)
        self.assertEqual('7', datamodle.incomming_key)

if __name__ == "__main__":
    unittest.main()
