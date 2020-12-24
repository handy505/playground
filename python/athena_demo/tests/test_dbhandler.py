import unittest
from unittest.mock import  MagicMock
from datetime import datetime

from dbhandler import DBHandler
from demo3 import Record 



class TestDBHandler(unittest.TestCase):

    def test_update_uploaded_row_by_uid(self):
        h = DBHandler(inmemory=True)
        records = [Record(1, datetime(2020,12,24,0,0,0), 88, 99),
                   Record(1, datetime(2020,12,24,0,0,0), 88, 99),
                   Record(1, datetime(2020,12,24,0,0,0), 88, 99),]
        [h.insert_record(r) for r in records]


        h.update_uploaded_row_by_uid(2)
        rows = h.read_unuploaded_rows()
        uids = [r[0] for r in rows]
        self.assertEqual(uids, [1,3])


    def test_2(self):
        h = DBHandler(inmemory=True)
        records = [Record(1, datetime(2020,12,24,0,0,0), 88, 99),
                   Record(1, datetime(2020,12,24,0,0,0), 88, 99),
                   Record(1, datetime(2020,12,24,0,0,0), 88, 99),]
        [h.insert_record(r) for r in records]

        h.update_uploaded_row_by_less_then_uid(2)
        rows = h.read_unuploaded_rows()
        uids = [r[0] for r in rows]
        self.assertEqual(uids, [3])


if __name__ == "__main__":
    unittest.main()
