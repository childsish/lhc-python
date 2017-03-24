import unittest

from lhc.interval import Interval
from lhc.indices.tracked_index import Track


@unittest.skip('obsolete and will be removed')
class TestEmptyTrackedIndex(unittest.TestCase):
    def test_get_cost_increase(self):
        track = Track(2)
        self.assertEqual(50, track.get_cost_increase(['chr1', Interval(0, 1000)]))

    def test_add(self):
        track = Track(2)
        track.add(['chr1', Interval(0, 1000)], 0)

        self.assertEqual([['chr1', 0]], track.starts)
        self.assertEqual([['chr1', 1000]], track.stops)
        self.assertEqual([[0, 0, 1]], track.offsets)


@unittest.skip('obsolete and will be removed')
class TestTrackIndex(unittest.TestCase):
    def setUp(self):
        self.track = Track(2)
        self.track.starts = [['chr1', 1000], ['chr1', 3000], ['chr2', 1000], ['chr2', 3000]]
        self.track.stops = [['chr1', 2000], ['chr1', 4000], ['chr2', 2000], ['chr2', 4000]]
        self.track.offsets = [[0, 2, 3], [3, 5, 3], [6, 8, 3], [9, 11, 3]]

    def test_fetch(self):
        self.assertEqual([[0, 2, 3], [3, 5, 3]], self.track.fetch('chr1', Interval(1750, 3250)))
        self.assertEqual([[0, 2, 3], [3, 5, 3]], self.track.fetch('chr1', 1750, 3250))

    def test_add_before(self):
        self.assertRaises(ValueError, self.track.add, ['chr1', Interval(0, 1000)], 12)

    def test_add_overlap_earlier_offset(self):
        self.assertRaises(ValueError, self.track.add, ['chr2', Interval(3500, 4500)], 11)

    def test_add_overlap(self):
        self.track.add(['chr2', Interval(3500, 4500)], 12)

        self.assertEqual([['chr1', 1000], ['chr1', 3000], ['chr2', 1000], ['chr2', 3000]], self.track.starts)
        self.assertEqual([['chr1', 2000], ['chr1', 4000], ['chr2', 2000], ['chr2', 4500]], self.track.stops)
        self.assertEqual([[0, 2, 3], [3, 5, 3], [6, 8, 3], [9, 12, 4]], self.track.offsets)

    def test_add_after(self):
        self.track.add(['chr2', Interval(5000, 6000)], 12)

        self.assertEqual([['chr1', 1000], ['chr1', 3000], ['chr2', 1000], ['chr2', 3000], ['chr2', 5000]], self.track.starts)
        self.assertEqual([['chr1', 2000], ['chr1', 4000], ['chr2', 2000], ['chr2', 4000], ['chr2', 6000]], self.track.stops)
        self.assertEqual([[0, 2, 3], [3, 5, 3], [6, 8, 3], [9, 11, 3], [12, 12, 1]], self.track.offsets)

    def test_get_cost_increase(self):
        self.assertRaises(ValueError, self.track.get_cost_increase, ['chr1', Interval(0, 1000)])
        self.assertAlmostEqual(3, self.track.get_cost_increase(['chr2', Interval(3500, 4500)]))
        self.assertAlmostEqual(0, self.track.get_cost_increase(['chr2', Interval(5000, 6000)]))

if __name__ == '__main__':
    unittest.main()
