import unittest

import StringIO

from lhc.io.fasta.iterator import FastaIterator, FastaLine


class TestIteratorWithThreshold(unittest.TestCase):
    def setUp(self):
        self.fileobj = StringIO.StringIO('>1\naaaaacccccgggggttttt\naaaaaccccc\naaaaacccc\n'
                                         '>2 a very large header\naaaaacccccgggggttttt\n')

    def test_iterator(self):
        iterator = FastaIterator(self.fileobj, 5)

        self.assertEqual(FastaLine('>1', 'aaaaa', 0, 5), iterator.next())
        self.assertEqual(FastaLine('>1', 'ccccc', 5, 10), iterator.next())
        self.assertEqual(FastaLine('>1', 'ggggg', 10, 15), iterator.next())
        self.assertEqual(FastaLine('>1', 'ttttt', 15, 20), iterator.next())
        self.assertEqual(FastaLine('>1', 'aaaaa', 20, 25), iterator.next())
        self.assertEqual(FastaLine('>1', 'ccccc', 25, 30), iterator.next())
        self.assertEqual(FastaLine('>1', 'aaaaa', 30, 35), iterator.next())
        self.assertEqual(FastaLine('>1', 'cccc', 35, 39), iterator.next())
        self.assertEqual(FastaLine('>2 a very large header', 'aaaaa', 0, 5), iterator.next())
        self.assertEqual(FastaLine('>2 a very large header', 'ccccc', 5, 10), iterator.next())
        self.assertEqual(FastaLine('>2 a very large header', 'ggggg', 10, 15), iterator.next())
        self.assertEqual(FastaLine('>2 a very large header', 'ttttt', 15, 20), iterator.next())


if __name__ == '__main__':
    unittest.main()
