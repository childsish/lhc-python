import unittest

from io import StringIO
from lhc.io.fasta.wrapper import FastaWrapper, SequenceFragment


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.fileobj = StringIO('>1\naaaaacccccgggggttttt\naaaaaccccc\naaaaacccc\n'
                                '>2 a very large header\naaaaacccccgggggttttt\n')

    def test_iterator_small_wrap(self):
        iterator = FastaWrapper(self.fileobj, 5)

        self.assertEqual(SequenceFragment('1', 'aaaaa', 0, 5), next(iterator))
        self.assertEqual(SequenceFragment('1', 'ccccc', 5, 10), next(iterator))
        self.assertEqual(SequenceFragment('1', 'ggggg', 10, 15), next(iterator))
        self.assertEqual(SequenceFragment('1', 'ttttt', 15, 20), next(iterator))
        self.assertEqual(SequenceFragment('1', 'aaaaa', 20, 25), next(iterator))
        self.assertEqual(SequenceFragment('1', 'ccccc', 25, 30), next(iterator))
        self.assertEqual(SequenceFragment('1', 'aaaaa', 30, 35), next(iterator))
        self.assertEqual(SequenceFragment('1', 'cccc', 35, 39), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'aaaaa', 0, 5), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'ccccc', 5, 10), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'ggggg', 10, 15), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'ttttt', 15, 20), next(iterator))
        self.assertRaises(StopIteration, next, iterator)

    def test_iterator_large_wrap(self):
        iterator = FastaWrapper(self.fileobj, 15)

        self.assertEqual(SequenceFragment('1', 'aaaaacccccggggg', 0, 15), next(iterator))
        self.assertEqual(SequenceFragment('1', 'tttttaaaaaccccc', 15, 30), next(iterator))
        self.assertEqual(SequenceFragment('1', 'aaaaacccc', 30, 39), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'aaaaacccccggggg', 0, 15), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'ttttt', 15, 20), next(iterator))
        self.assertRaises(StopIteration, next, iterator)

    def test_iterator_small_chunk_size(self):
        iterator = FastaWrapper(self.fileobj, 15, chunk_size=10)

        self.assertEqual(SequenceFragment('1', 'aaaaacccccggggg', 0, 15), next(iterator))
        self.assertEqual(SequenceFragment('1', 'tttttaaaaaccccc', 15, 30), next(iterator))
        self.assertEqual(SequenceFragment('1', 'aaaaacccc', 30, 39), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'aaaaacccccggggg', 0, 15), next(iterator))
        self.assertEqual(SequenceFragment('2 a very large header', 'ttttt', 15, 20), next(iterator))
        self.assertRaises(StopIteration, next, iterator)


if __name__ == '__main__':
    unittest.main()
