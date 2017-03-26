import unittest

from lhc.collections import IntervalMap
from lhc.interval import Interval


class TestIntervalMap(unittest.TestCase):
    def test_add(self):
        map_ = IntervalMap()

        map_[Interval(0, 1000)] = 1

        self.assertEqual(1, len(map_))
        self.assertTrue(any(Interval(0, 1000) in bin for bin in map_.bins.values()))
        self.assertTrue(any(1 in value for value in map_.values.values()))

    def test_init(self):
        map_ = IntervalMap([(Interval(0, 1000), 1), (Interval(1000, 2000), 2), (Interval(2000, 3000), 3)])

        self.assertEqual(3, len(map_))
        self.assertTrue(any(Interval(0, 1000) in bin for bin in map_.bins.values()))
        self.assertTrue(any(1 in values for values in map_.values.values()))
        self.assertTrue(any(Interval(1000, 2000) in bin for bin in map_.bins.values()))
        self.assertTrue(any(2 in values for values in map_.values.values()))
        self.assertTrue(any(Interval(2000, 3000) in bin for bin in map_.bins.values()))
        self.assertTrue(any(3 in values for values in map_.values.values()))

    def test_contains(self):
        map_ = IntervalMap([(Interval(0, 1000), 1), (Interval(1000, 2000), 2), (Interval(2000, 3000), 3)])

        self.assertIn(Interval(0, 1000), map_)
        self.assertIn(Interval(1000, 2000), map_)
        self.assertIn(Interval(2000, 3000), map_)

    def test_fetch(self):
        map_ = IntervalMap([(Interval(0, 1000), 1), (Interval(1000, 2000), 2), (Interval(2000, 3000), 3)])

        it = map_[Interval(500, 1500)]

        self.assertEqual(1, next(it))
        self.assertEqual(2, next(it))
        self.assertRaises(StopIteration, it.__next__)


if __name__ == '__main__':
    unittest.main()
