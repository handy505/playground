import unittest
from unittest.mock import  MagicMock
from datetime import datetime


from simplecorn import Job

def action1():
    print('action1')


def action2():
    print('action2')


class TestSimpleCron(unittest.TestCase):

    def test_1(self):
        j = Job('* * * * *', action1)

        j.get_datetime = MagicMock(return_value=datetime(2020, 12, 23, 12, 0, 0))
        result = j.is_established()
        self.assertEqual(True, result)


    def test_2(self):
        j = Job('1,2,3 * * * *', action1)
        j.get_datetime = MagicMock(return_value=datetime(2020, 12, 23, 12, 1, 0))

        result = j.is_established()
        self.assertEqual(True, result)


    def test_3(self):
        j = Job('1,2,3 * * * *', action1)
        j.get_datetime = MagicMock(return_value=datetime(2020, 12, 23, 12, 0, 0))

        result = j.is_established()
        self.assertEqual(False, result)

if __name__ == "__main__":
    unittest.main()
