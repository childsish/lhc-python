import unittest

from lhc.io.fasta.iterator import FastaEntryIterator


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
        it = FastaEntryIterator(iter(self.lines))
        
        self.assertEqual(tuple(next(it)), ('a x', 'aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee'))
        self.assertEqual(tuple(next(it)), ('b y', 'ffffffffffgggggggggghhhhh'))
        self.assertRaises(StopIteration, it.__next__)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
