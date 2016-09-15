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

        self.assertEqual(set_.fetch(0, 10), [])
        self.assertEqual(set_.fetch(5, 15), [Interval(10, 20)])
        self.assertEqual(set_.fetch(15, 25), [Interval(10, 20)])
        self.assertEqual(set_.fetch(20, 30), [])
        self.assertEqual(set_.fetch(30, 70), [Interval(30, 50), Interval(40, 60)])
        self.assertEqual(set_.fetch(30, 40), [Interval(30, 50)])
        self.assertEqual(set_.fetch(40, 50), [Interval(30, 50), Interval(40, 60)])
        self.assertEqual(set_.fetch(50, 60), [Interval(40, 60)])
        self.assertEqual(set_.fetch(70, 80), [Interval(70, 100)])
        self.assertEqual(set_.fetch(80, 90), [Interval(70, 100), Interval(80, 90)])
        self.assertEqual(set_.fetch(90, 100), [Interval(70, 100)])

    def test_getByKeyInterval(self):
        set_ = InOrderAccessIntervalSet(iter(self.key_intervals), key=lambda x: Interval((x[0], x[1]), (x[0], x[2])))

        self.assertEqual(set_.fetch('chr1', 0, 10), [('chr1', 0, 10, 'idq')])
        self.assertEqual(set_.fetch('chr1', 0, 50), [('chr1', 0, 10, 'idq'),
                                                      ('chr1', 20, 40, 'idw'),
                                                      ('chr1', 30, 50, 'ide')])
        self.assertEqual(set_.fetch('chr2', 10, 20), [])
        self.assertEqual(set_.fetch('chr2', 20, 30), [('chr2', 20, 40, 'idt')])
        self.assertEqual(set_.fetch('chr2', 30, 40), [('chr2', 20, 40, 'idt'),
                                                       ('chr2', 30, 50, 'idy')])
        self.assertEqual(set_.fetch('chr2', 40, 50), [('chr2', 30, 50, 'idy')])

if __name__ == '__main__':
    unittest.main()
