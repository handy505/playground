#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import crc


class TestCRC(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_crc16(self):
        seq = [0x01, 0x03, 0xc0, 0x20, 0x00, 0x18]
        b2, b1 = crc.crc16(seq)

        self.assertEqual(b2, 0x78)
        self.assertEqual(b1, 0xa)


    def test_crc16_with_append(self):
        seq = [0x01, 0x03, 0xc0, 0x20, 0x00, 0x18]
        b2, b1 = crc.crc16(seq, append=True)

        self.assertEqual(b2, 0x78)
        self.assertEqual(b1, 0xa)

        expect = [0x01, 0x03, 0xc0, 0x20, 0x00, 0x18, 0x78, 0xa]
        self.assertEqual(seq, expect)


if __name__ == "__main__":
    unittest.main()
