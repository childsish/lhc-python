import unittest

from lhc.io import iter_bed


class TestBed(unittest.TestCase):
    def setUp(self):
        self.content = '''chr1\t100\t200\t_00\t0.0\t+
chr1\t150\t250\t_01\t0.0\t+
chr1\t200\t300\t_02\t0.0\t+
chr2\t100\t200\t_03\t0.0\t+
chr2\t150\t250\t_04\t0.0\t+
chr2\t200\t300\t_05\t0.0\t+
'''

    @unittest.skip("skip until chromosome_id fixed")
    def test_iterator(self):
        it = iter_bed(self.content.split('\n'))

        i = next(it)
        self.assertEqual(('chr1', 99, 200), (i.chromosome, i.start.position, i.stop.position))
        i = next(it)
        self.assertEqual(('chr1', 149, 250), (i.chromosome, i.start.position, i.stop.position))
        i = next(it)
        self.assertEqual(('chr1', 199, 300), (i.chromosome, i.start.position, i.stop.position))
        i = next(it)
        self.assertEqual(('chr2', 99, 200), (i.chromosome, i.start.position, i.stop.position))
        i = next(it)
        self.assertEqual(('chr2', 149, 250), (i.chromosome, i.start.position, i.stop.position))
        i = next(it)
        self.assertEqual(('chr2', 199, 300), (i.chromosome, i.start.position, i.stop.position))
        self.assertRaises(StopIteration, next, it)
        
if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
