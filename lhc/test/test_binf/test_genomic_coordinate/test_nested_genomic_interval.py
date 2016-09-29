import unittest

from lhc.binf.genomic_coordinate import GenomicInterval as Interval, NestedGenomicInterval as NestedInterval


class TestNestedGenomicInterval(unittest.TestCase):
    def test_get_sub_seq(self):
        seq = {'1': 'aquickbrownfoxjumpsoverthelazydog'}
        ni = NestedInterval('1', 5, 25)
        ni.children = [Interval('1', 5, 10), Interval('1', 20, 25)]

        self.assertEqual('kbrowverth', ni.get_sub_seq(seq))

    def test_get_sub_seq_complement(self):
        seq = {'1': 'aquickbrownfoxjumpsoverthelazydog'}
        ni = NestedInterval('1', 5, 25, strand='-')
        ni.children = [Interval('1', 5, 10), Interval('1', 20, 25)]

        self.assertEqual('dayebwoyvm', ni.get_sub_seq(seq))

    def test_get_sub_seq_complement_complement(self):
        seq = {'1': 'aquickbrownfoxjumpsoverthelazydog'}
        ni = NestedInterval('1', 5, 25, strand='-')
        ni.children = [Interval('1', 5, 10, strand='-'), Interval('1', 20, 25, strand='-')]

        self.assertEqual('verthkbrow', ni.get_sub_seq(seq))


if __name__ == '__main__':
    unittest.main()
