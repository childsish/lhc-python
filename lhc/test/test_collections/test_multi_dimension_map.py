__author__ = 'Liam Childs'

import unittest

from lhc.collections import MultiDimensionMap, IntervalMap
from lhc.interval import Interval


class TestMultiDimensionMap(unittest.TestCase):
    def test_add(self):
        map_ = MultiDimensionMap([str, Interval])

        map_[['Chr1', Interval(0, 1000)]] = 1

        self.assertEqual(1, len(map_))
        self.assertFalse(map_.root.is_last)
        self.assertIs(type(map_.root.map), dict)
        self.assertIs(type(map_.root.map['Chr1'].map), IntervalMap)
        self.assertIn(Interval(0, 1000), list(map_.root.map['Chr1'].map.bins.values())[0])
        self.assertIn(1, list(map_.root.map['Chr1'].map.values.values())[0])

    def test_init(self):
        map_ = MultiDimensionMap([str, Interval], [(('Chr1', Interval(1000, 2000)), 1),
                                                   (('Chr1', Interval(3000, 4000)), 2),
                                                   (('Chr2', Interval(1000, 2000)), 3),
                                                   (('Chr2', Interval(3000, 4000)), 4)])

        self.assertEqual(4, len(map_))
        self.assertEqual({'Chr1', 'Chr2'}, set(map_.root.map))

    def test_fetch(self):
        map_ = MultiDimensionMap([str, Interval], [(('Chr1', Interval(1000, 2000)), 1),
                                                   (('Chr1', Interval(3000, 4000)), 2),
                                                   (('Chr2', Interval(1000, 2000)), 3),
                                                   (('Chr2', Interval(3000, 4000)), 4)])

        it = map_[('Chr2', Interval(1500, 3500))]

        self.assertEqual(3, next(it))
        self.assertEqual(4, next(it))
        self.assertRaises(StopIteration, it.__next__)


if __name__ == '__main__':
    unittest.main()
