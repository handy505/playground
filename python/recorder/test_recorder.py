#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

import recorder 


class TestRecorder(unittest.TestCase):
    
    def setUp(self):
        lines = [
            '1,2017/01/01 00:00:00,1000\n',
            '2,2017/01/01 00:01:00,1001\n',
            '3,2017/01/01 00:02:00,1002\n',
            '4,2017/01/01 00:03:00,1003\n',
            '5,2017/01/01 00:04:00,1004\n',
            '6,2017/01/01 00:05:00,1005\n',
            '7,2017/01/01 00:06:00,1006\n'
        ]
        with open('./minute.txt', 'w', encoding='utf-8') as fw:
            fw.writelines(lines)

        self.datamodle = recorder.LogModle('./minute.txt')


    def tearDown(self):
        os.system('rm ./minute.txt')


    def test_record_modle(self):

        rec = self.datamodle.dc.get('1')
        self.assertEqual('1,2017/01/01 00:00:00,1000', rec)

        self.assertEqual(7, len(self.datamodle.dc))
        self.assertEqual('1', self.datamodle.uploading_key)
        self.assertEqual('7', self.datamodle.incomming_key)

if __name__ == "__main__":
    unittest.main()
