import unittest

from io import StringIO
from lhc.binf.genomic_coordinate import GenomicInterval as Interval
from lhc.io.fasta.wrapper import FastaWrapper


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.fileobj = StringIO('>1\naaaaacccccgggggttttt\naaaaaccccc\naaaaacccc\n'
                                '>2 a very large header\naaaaacccccgggggttttt\n')

    def test_iterator_small_wrap(self):
        iterator = FastaWrapper(self.fileobj, 5)

        self.assertEqual(Interval(0, 5, chromosome='1', data='aaaaa'), next(iterator))
        self.assertEqual(Interval(5, 10, chromosome='1', data='ccccc'), next(iterator))
        self.assertEqual(Interval(10, 15, chromosome='1', data='ggggg'), next(iterator))
        self.assertEqual(Interval(15, 20, chromosome='1', data='ttttt'), next(iterator))
        self.assertEqual(Interval(20, 25, chromosome='1', data='aaaaa'), next(iterator))
        self.assertEqual(Interval(25, 30, chromosome='1', data='ccccc'), next(iterator))
        self.assertEqual(Interval(30, 35, chromosome='1', data='aaaaa'), next(iterator))
        self.assertEqual(Interval(35, 39, chromosome='1', data='cccc'), next(iterator))
        self.assertEqual(Interval(0, 5, chromosome='2 a very large header', data='aaaaa'), next(iterator))
        self.assertEqual(Interval(5, 10, chromosome='2 a very large header', data='ccccc'), next(iterator))
        self.assertEqual(Interval(10, 15, chromosome='2 a very large header', data='ggggg'), next(iterator))
        self.assertEqual(Interval(15, 20, chromosome='2 a very large header', data='ttttt'), next(iterator))
        self.assertRaises(StopIteration, next, iterator)

    def test_iterator_large_wrap(self):
        iterator = FastaWrapper(self.fileobj, 15)

        self.assertEqual(Interval(0, 15, chromosome='1', data='aaaaacccccggggg'), next(iterator))
        self.assertEqual(Interval(15, 30, chromosome='1', data='tttttaaaaaccccc'), next(iterator))
        self.assertEqual(Interval(30, 39, chromosome='1', data='aaaaacccc'), next(iterator))
        self.assertEqual(Interval(0, 15, chromosome='2 a very large header', data='aaaaacccccggggg'), next(iterator))
        self.assertEqual(Interval(15, 20, chromosome='2 a very large header', data='ttttt'), next(iterator))
        self.assertRaises(StopIteration, next, iterator)

    def test_iterator_small_chunk_size(self):
        iterator = FastaWrapper(self.fileobj, 15, chunk_size=10)

        self.assertEqual(Interval(0, 15, chromosome='1', data='aaaaacccccggggg'), next(iterator))
        self.assertEqual(Interval(15, 30, chromosome='1', data='tttttaaaaaccccc'), next(iterator))
        self.assertEqual(Interval(30, 39, chromosome='1', data='aaaaacccc'), next(iterator))
        self.assertEqual(Interval(0, 15, chromosome='2 a very large header', data='aaaaacccccggggg'), next(iterator))
        self.assertEqual(Interval(15, 20, chromosome='2 a very large header', data='ttttt'), next(iterator))
        self.assertRaises(StopIteration, next, iterator)


if __name__ == '__main__':
    unittest.main()
