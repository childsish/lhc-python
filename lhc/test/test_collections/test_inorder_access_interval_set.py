import unittest

from lhc.interval import Interval
from lhc.collections.inorder_access_interval_set import InOrderAccessIntervalSet


class TestInOrderAccessIntervalSet(unittest.TestCase):
    def setUp(self):
        self.intervals = [
            Interval(10, 20),
            Interval(30, 50),
            Interval(40, 60),
            Interval(70, 100),
            Interval(80, 90)
        ]
        self.key_intervals = [
            ('chr1', 0, 10, 'idq'),
            ('chr1', 20, 40, 'idw'),
            ('chr1', 30, 50, 'ide'),
            ('chr2', 0, 10, 'idr'),
            ('chr2', 20, 40, 'idt'),
            ('chr2', 30, 50, 'idy')
        ]

    def test_getByInterval(self):
        set_ = InOrderAccessIntervalSet(iter(self.intervals))

        self.assertEqual(set_[Interval(0, 10)], [])
        self.assertEqual(set_[Interval(5, 15)], [Interval(10, 20)])
        self.assertEqual(set_[Interval(15, 25)], [Interval(10, 20)])
        self.assertEqual(set_[Interval(20, 30)], [])
        self.assertEqual(set_[Interval(30, 40)], [Interval(30, 50)])
        self.assertEqual(set_[Interval(30, 70)], [Interval(30, 50), Interval(40, 60)])
        self.assertEqual(set_[Interval(40, 50)], [Interval(30, 50), Interval(40, 60)])
        self.assertEqual(set_[Interval(50, 60)], [Interval(40, 60)])
        self.assertEqual(set_[Interval(70, 80)], [Interval(70, 100)])
        self.assertEqual(set_[Interval(80, 90)], [Interval(70, 100), Interval(80, 90)])
        self.assertEqual(set_[Interval(90, 100)], [Interval(70, 100)])

if __name__ == '__main__':
    unittest.main()
