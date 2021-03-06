import unittest

from lhc.binf.genomic_coordinate import GenomicPosition


class TestGenomicPosition(unittest.TestCase):
    def test_eq(self):
        a = GenomicPosition('1', 0)
        b = GenomicPosition('1', 0)
        c = GenomicPosition('1', 1)
        d = GenomicPosition('2', 0)

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)

    def test_lt(self):
        a = GenomicPosition('1', 0)
        b = GenomicPosition('1', 0)
        c = GenomicPosition('1', 1)
        d = GenomicPosition('2', 0)

        self.assertFalse(a < b)
        self.assertLess(a, c)
        self.assertLess(a, d)

    def test_get_distance(self):
        a = GenomicPosition('1', 0)
        b = GenomicPosition('1', 0)
        c = GenomicPosition('1', 1)
        d = GenomicPosition('2', 0)

        self.assertEqual(0, b.get_distance_to(a))
        self.assertEqual(1, c.get_distance_to(a))
        self.assertRaises(ValueError, d.get_distance_to, a)


if __name__ == '__main__':
    unittest.main()
