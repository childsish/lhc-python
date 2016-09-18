import unittest

from lhc.binf.genomic_coordinate import GenomicInterval as I, NestedGenomicInterval as NI


class TestNestedGenomicInterval(unittest.TestCase):
    def test_get_sub_seq(self):
        seq = {'1': 'aquickbrownfoxjumpsoverthelazydog'}
        ni = NI([I('1', 5, 10), I('1', 20, 25)])

        self.assertEqual('kbrowverth', ni.get_sub_seq(seq))

    def test_get_sub_seq_complement(self):
        seq = {'1': 'aquickbrownfoxjumpsoverthelazydog'}
        ni = NI([I('1', 5, 10), I('1', 20, 25)], strand='-')

        self.assertEqual('dayebwoyvm', ni.get_sub_seq(seq))

    def test_get_sub_seq_complement_complement(self):
        seq = {'1': 'aquickbrownfoxjumpsoverthelazydog'}
        ni = NI([I('1', 5, 10, strand='-'), I('1', 20, 25, strand='-')], strand='-')

        self.assertEqual('verthkbrow', ni.get_sub_seq(seq))


if __name__ == '__main__':
    unittest.main()
