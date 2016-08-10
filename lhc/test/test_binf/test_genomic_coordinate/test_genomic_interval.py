import unittest

from lhc.binf.genomic_coordinate import GenomicInterval as Interval


class TestGenomicInterval(unittest.TestCase):
    def test_comparisons(self):
        a = Interval('1', 0, 10)
        b = Interval('1', 5, 10)
        c = Interval('1', 5, 15)
        d = Interval('2', 0, 10)

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
        interval = Interval('chr1', 1000, 2000)
        pickled_feature = pickle.dumps(interval)

        self.assertEqual(interval, pickle.loads(pickled_feature))

if __name__ == '__main__':
    unittest.main()
