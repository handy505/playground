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
            '7,2017/01/01 00:06:00,1006\n']
        with open('./minute.txt', 'w', encoding='utf-8') as fw:
            fw.writelines(lines)

        self.mydb = recorder.UidDatabase('./minute.txt')


    def tearDown(self):
        os.system('rm ./minute.txt')


    def test_append_record(self):
        self.mydb.append_record('8,2017/01/01 00:07:00,1007')
        self.assertEqual(8, len(self.mydb.data))
        self.assertEqual(1, self.mydb.processing_key)
        self.assertEqual(8, self.mydb.incomming_key)

        self.mydb.append_record('9,2017/01/01 00:07:00,1008')
        self.assertEqual(9, len(self.mydb.data))
        self.assertEqual(1, self.mydb.processing_key)
        self.assertEqual(9, self.mydb.incomming_key)


    def test_get_record(self):
        rec = self.mydb.get_record_step_ahead()
        self.assertEqual('1,2017/01/01 00:00:00,1000', rec)
        self.assertEqual(7, len(self.mydb.data))
        self.assertEqual(2, self.mydb.processing_key)
        self.assertEqual(7, self.mydb.incomming_key)

        rec = self.mydb.get_record_step_ahead()
        self.assertEqual('2,2017/01/01 00:01:00,1001', rec)
        self.assertEqual(7, len(self.mydb.data))
        self.assertEqual(3, self.mydb.processing_key)
        self.assertEqual(7, self.mydb.incomming_key)

        rec = self.mydb.get_record_step_ahead()
        rec = self.mydb.get_record_step_ahead()
        rec = self.mydb.get_record_step_ahead()
        rec = self.mydb.get_record_step_ahead()
        rec = self.mydb.get_record_step_ahead()
        self.assertEqual('7,2017/01/01 00:06:00,1006', rec)
        self.assertEqual(7, len(self.mydb.data))
        self.assertEqual(8, self.mydb.processing_key)
        self.assertEqual(7, self.mydb.incomming_key)

        rec = self.mydb.get_record_step_ahead()
        self.assertEqual(None, rec)
        self.assertEqual(7, len(self.mydb.data))
        self.assertEqual(8, self.mydb.processing_key)
        self.assertEqual(7, self.mydb.incomming_key)

        rec = self.mydb.get_record_step_ahead()
        self.assertEqual(None, rec)
        self.assertEqual(7, len(self.mydb.data))
        self.assertEqual(8, self.mydb.processing_key)
        self.assertEqual(7, self.mydb.incomming_key)


    def test_delete_record(self):
        self.mydb.delete_record(1)
        self.assertEqual(6, len(self.mydb.data))
        self.mydb.delete_record(1)
        self.assertEqual(6, len(self.mydb.data))
        self.mydb.delete_record(2)
        self.assertEqual(5, len(self.mydb.data))


if __name__ == "__main__":
    unittest.main()
