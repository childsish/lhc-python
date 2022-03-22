import unittest

from lhc.binf.genomic_coordinate import GenomicInterval as Interval, NestedGenomicInterval as NestedInterval
from lhc.collections import SequenceSet


class TestNestedGenomicInterval(unittest.TestCase):
    def test_get_sub_seq(self):
        seq = SequenceSet({'1': 'aaaaccccggggttttaaaaccccggggtttt'})
        ni = NestedInterval(5, 25, chromosome='1')
        ni.children = [NestedInterval(5, 10, chromosome='1'), NestedInterval(20, 25, chromosome='1')]

        self.assertEqual('cccggccccg', ni.get_sub_seq(seq))

    def test_get_sub_seq_complement(self):
        seq = SequenceSet({'1': 'aaaaccccggggttttaaaaccccggggtttt'})
        ni = NestedInterval(5, 25, chromosome='1', strand='-')
        ni.children = [NestedInterval(5, 10, chromosome='1'), NestedInterval(20, 25, chromosome='1')]

        self.assertEqual('cggggccggg', ni.get_sub_seq(seq))

    def test_get_sub_seq_complement_complement(self):
        seq = SequenceSet({'1': 'aaaaccccggggttttaaaaccccggggtttt'})
        ni = NestedInterval(5, 25, chromosome='1', strand='-')
        ni.children = [NestedInterval(5, 10, chromosome='1', strand='-'), NestedInterval(20, 25, chromosome='1', strand='-')]

        self.assertEqual('ccccgcccgg', ni.get_sub_seq(seq))


if __name__ == '__main__':
    unittest.main()
