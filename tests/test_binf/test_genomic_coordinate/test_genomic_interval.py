import unittest

from lhc.entities.genomic_coordinate import GenomicInterval as Interval


class TestGenomicInterval(unittest.TestCase):
    def test_comparisons(self):
        a = Interval(0, 10, chromosome='1')
        b = Interval(5, 10, chromosome='1')
        c = Interval(5, 15, chromosome='1')
        d = Interval(0, 10, chromosome='2')

        self.assertTrue(a == a)
        self.assertFalse(a == b)
        self.assertFalse(b == a)
        
        self.assertTrue(a < b)
        self.assertFalse(b < a)
        self.assertTrue(b < c)
        self.assertFalse(c < b)
        
        self.assertFalse(a == d)
        self.assertFalse(d == a)

    def test_is_picklable(self):
        import pickle
        interval = Interval(1000, 2000, chromosome='chr1')
        pickled_feature = pickle.dumps(interval)

        self.assertEqual(interval, pickle.loads(pickled_feature))

if __name__ == '__main__':
    unittest.main()
