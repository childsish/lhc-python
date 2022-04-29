import unittest

from lhc.entities.interval import Interval
from lhc.entities.interval.set_operations import multi_difference, set_intersect


class TestSetOperations(unittest.TestCase):
    def test_multi_difference(self):
        self.assertListEqual([Interval(20, 30)], multi_difference(Interval(20, 30), [Interval(-20, -10)]))
        self.assertListEqual([Interval(20, 30)], multi_difference(Interval(20, 30), [Interval(40, 50)]))
        self.assertListEqual([Interval(20, 22), Interval(28, 30)], multi_difference(Interval(20, 30), [Interval(22, 28)]))
        self.assertListEqual([Interval(20, 21), Interval(22, 23), Interval(24, 25), Interval(26, 27), Interval(28, 29)],
                             multi_difference(Interval(20, 30), [Interval(21, 22), Interval(23, 24), Interval(25, 26), Interval(27, 28), Interval(29, 30)]))

    def test_set_intersect(self):
        self.assertListEqual([Interval(15, 25), Interval(25, 30)], list(set_intersect(
            [Interval(20, 30)],
            [Interval(0, 10), Interval(10, 20), Interval(15, 25), Interval(25, 30), Interval(30, 35), Interval(35, 40)]
        )))
        self.assertListEqual([Interval(20, 25), Interval(25, 30)], list(set_intersect(
            [Interval(20, 30)],
            [Interval(0, 10), Interval(10, 20), Interval(15, 25), Interval(25, 30), Interval(30, 35), Interval(35, 40)],
            intersect_intervals=True
        )))
