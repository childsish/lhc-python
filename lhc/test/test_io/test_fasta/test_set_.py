import unittest

from lhc.binf.genomic_coordinate import GenomicPosition as Position, GenomicInterval as Interval
from lhc.io.fasta import FastaIterator
from lhc.io.fasta.set_ import FastaSet


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
                      'hhhhh\n']

    def test_getItemByKey(self):
        parser = FastaSet(FastaIterator(iter(self.lines)))

        self.assertEqual(parser['a'], 'aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee')
        self.assertEqual(parser['b'], 'ffffffffffgggggggggghhhhh')

    def test_getItemSinglePosition(self):
        parser = FastaSet(FastaIterator(iter(self.lines)))

        self.assertEqual(parser[Position('a', 10)], 'b')
        self.assertEqual(parser[Position('b', 10)], 'g')

    def test_getItemInterval(self):
        parser = FastaSet(FastaIterator(iter(self.lines)))

        self.assertEqual(parser[Interval(10, 20, chromosome='a')], 'bbbbbbbbbb')
        self.assertEqual(parser[Interval(10, 20, chromosome='b')], 'gggggggggg')
        self.assertEqual(parser[Interval(5, 15, chromosome='a')], 'aaaaabbbbb')
        self.assertEqual(parser[Interval(5, 15, chromosome='b')], 'fffffggggg')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
