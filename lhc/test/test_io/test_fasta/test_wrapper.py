import unittest

from io import StringIO
from lhc.binf.genomic_coordinate import GenomicPosition
from lhc.io.fasta.wrapper import FastaWrapper, SequenceFragment


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.fileobj = StringIO('>1\naaaaacccccgggggttttt\naaaaaccccc\naaaaacccc\n'
                                '>2 a very large header\naaaaacccccgggggttttt\n')

    def test_iterator_small_wrap(self):
        iterator = FastaWrapper(self.fileobj, 5)

        self.assertEqual(SequenceFragment(GenomicPosition('1', 0), GenomicPosition('1', 5), 'aaaaa'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 5), GenomicPosition('1', 10), 'ccccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 10), GenomicPosition('1', 15), 'ggggg'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 15), GenomicPosition('1', 20), 'ttttt'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 20), GenomicPosition('1', 25), 'aaaaa'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 25), GenomicPosition('1', 30), 'ccccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 30), GenomicPosition('1', 35), 'aaaaa'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 35), GenomicPosition('1', 39), 'cccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 0),
                                          GenomicPosition('2 a very large header', 5), 'aaaaa'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 5),
                                          GenomicPosition('2 a very large header', 10), 'ccccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 10),
                                          GenomicPosition('2 a very large header', 15), 'ggggg'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 15),
                                          GenomicPosition('2 a very large header', 20), 'ttttt'), next(iterator))
        self.assertRaises(StopIteration, next, iterator)

    def test_iterator_large_wrap(self):
        iterator = FastaWrapper(self.fileobj, 15)

        self.assertEqual(SequenceFragment(GenomicPosition('1', 0,),
                                          GenomicPosition('1', 15), 'aaaaacccccggggg'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 15),
                                          GenomicPosition('1', 30), 'tttttaaaaaccccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 30),
                                          GenomicPosition('1', 39), 'aaaaacccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 0),
                                          GenomicPosition('2 a very large header', 15),
                                          'aaaaacccccggggg'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 15),
                                          GenomicPosition('2 a very large header', 20),
                                          'ttttt'), next(iterator))
        self.assertRaises(StopIteration, next, iterator)

    def test_iterator_small_chunk_size(self):
        iterator = FastaWrapper(self.fileobj, 15, chunk_size=10)

        self.assertEqual(SequenceFragment(GenomicPosition('1', 0),
                                          GenomicPosition('1', 15), 'aaaaacccccggggg'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 15),
                                          GenomicPosition('1', 30), 'tttttaaaaaccccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('1', 30),
                                          GenomicPosition ('1', 39), 'aaaaacccc'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 0),
                                          GenomicPosition('2 a very large header', 15),
                                          'aaaaacccccggggg'), next(iterator))
        self.assertEqual(SequenceFragment(GenomicPosition('2 a very large header', 15),
                                          GenomicPosition('2 a very large header', 20), 'ttttt'), next(iterator))
        self.assertRaises(StopIteration, next, iterator)


if __name__ == '__main__':
    unittest.main()
