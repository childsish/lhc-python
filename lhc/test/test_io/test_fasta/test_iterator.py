import unittest

from lhc.io.fasta import FastaIterator, FastaFragmentIterator
from lhc.binf.genomic_coordinate import GenomicPosition


class TestFasta(unittest.TestCase):
    
    def setUp(self):
        self.lines = ['>a x\n',
                      'aaaaaaaaaa\n',
                      'bbbbbbbbbb\n',
                      'cccccccccc\n',
                      'dddddddddd\n',
                      'eeeeeeeeee\n',
                      '>b y\n',
                      'ffffffffff\n',
                      'gggggggggg\n',
                      'hhhhh']

    def test_iterEntries(self):
        it = FastaIterator(iter(self.lines))
        
        self.assertEqual(tuple(next(it)), ('a x', 'aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee'))
        self.assertEqual(tuple(next(it)), ('b y', 'ffffffffffgggggggggghhhhh'))
        self.assertRaises(StopIteration, next, it)

    def test_fragment_iterator(self):
        it = FastaFragmentIterator(iter(self.lines))

        results = list(it)

        self.assertEqual(GenomicPosition('a x', 0), results[0].start)
        self.assertEqual('aaaaaaaaaa', results[0].data)
        self.assertEqual(GenomicPosition('a x', 10), results[1].start)
        self.assertEqual(GenomicPosition('a x', 20), results[2].start)
        self.assertEqual(GenomicPosition('a x', 30), results[3].start)
        self.assertEqual(GenomicPosition('a x', 40), results[4].start)
        self.assertEqual(GenomicPosition('b y', 0), results[5].start)
        self.assertEqual(GenomicPosition('b y', 10), results[6].start)
        self.assertEqual(GenomicPosition('b y', 20), results[7].start)
        self.assertEqual('hhhhh', results[7].data)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
