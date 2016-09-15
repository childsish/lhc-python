__author__ = 'Liam Childs'

import unittest

from lhc.collections import IntervalSet
from lhc.interval import Interval


class TestIntervalSet(unittest.TestCase):
    def test_add(self):
        set_ = IntervalSet()

        set_.add(Interval(0, 1000))

        self.assertEqual(1, len(set_))
        self.assertTrue(any(Interval(0, 1000) in bin for bin in set_.bins.values()))

    def test_init(self):
        set_ = IntervalSet([Interval(0, 1000), Interval(1000, 2000), Interval(2000, 3000)])

        self.assertEqual(3, len(set_))
        self.assertTrue(any(Interval(0, 1000) in bin for bin in set_.bins.values()))
        self.assertTrue(any(Interval(1000, 2000) in bin for bin in set_.bins.values()))
        self.assertTrue(any(Interval(2000, 3000) in bin for bin in set_.bins.values()))

    def test_contains(self):
        set_ = IntervalSet([Interval(0, 1000), Interval(1000, 2000), Interval(2000, 3000)])

        self.assertIn(Interval(0, 1000), set_)
        self.assertIn(Interval(1000, 2000), set_)
        self.assertIn(Interval(2000, 3000), set_)

    def test_fetch(self):
        set_ = IntervalSet([Interval(0, 1000), Interval(1000, 2000), Interval(2000, 3000)])

        it = set_.fetch(Interval(500, 1500))

        self.assertEqual(Interval(0, 1000), next(it))
        self.assertEqual(Interval(1000, 2000), next(it))
        self.assertRaises(StopIteration, it.__next__)


if __name__ == '__main__':
    unittest.main()
