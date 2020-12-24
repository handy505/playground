import unittest
from unittest.mock import  MagicMock
from datetime import datetime

from simplecron import Job

def action1():
    print('action1')


def action2():
    print('action2')


class TestSimpleCron(unittest.TestCase):

    def test_is_established_every_minute(self):
        j = Job('* * * * *', action1)

        j.get_datetime = MagicMock(return_value=datetime(2020, 12, 23, 12, 0, 0))
        result = j.is_established()
        self.assertEqual(True, result)


    def test_is_established_on_indicate_minute(self):
        j = Job('1,2,3 * * * *', action1)
        j.get_datetime = MagicMock(return_value=datetime(2020, 12, 23, 12, 1, 0))

        result = j.is_established()
        self.assertEqual(True, result)


    def test_is_not_established_on_indicate_minute(self):
        j = Job('1,2,3 * * * *', action1)
        j.get_datetime = MagicMock(return_value=datetime(2020, 12, 23, 12, 0, 0))

        result = j.is_established()
        self.assertEqual(False, result)


    def test_is_established_on_divided_minute(self):
        j = Job('*/5 * * * *', action1)
        expect_conditions = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

        self.assertEqual(expect_conditions, j.minute_conditions)


    def test_is_established_on_divided_hour(self):
        j = Job('* */3 * * *', action1)
        expect_conditions = [0, 3, 6, 9, 12, 15, 18, 21]
        self.assertEqual(expect_conditions, j.hour_conditions)


    def test_is_established_on_divided_day(self):
        j = Job('* * */2 * *', action1)
        expect_conditions = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
        self.assertEqual(expect_conditions, j.day_conditions)


    def test_is_established_on_divided_month(self):
        j = Job('* * * */2 *', action1)
        expect_conditions = [2, 4, 6, 8, 10, 12]
        self.assertEqual(expect_conditions, j.month_conditions)


    def test_is_established_on_divided_weekday(self):
        j = Job('* * * * */2', action1)
        expect_conditions = [0, 2, 4, 6]
        self.assertEqual(expect_conditions, j.weekday_conditions)


if __name__ == "__main__":
    unittest.main()

