import unittest

from lhc.io.sequence.embl import EmblFile


class TestEmblFile(unittest.TestCase):
    def test_iter(self):
        embl_file = EmblFile()
        embl_file.file = iter([
            ';ID   L1HS        DNA   ; PRI   ; 6064 BP\n',
            ';FT   CDS           908..1921',
            ';FT                 /product="L1HS_1p"',
            ';FT   CDS           1988..5812',
            ';FT                 /product="L1HS_2p"',
            ';SQ   Sequence 6064 BP; 2341 A; 1339 C; 1230 G; 1154 T; 0 other;',
            'L1HS',
            'gggaggaggagccaagatggccgaataggaacagctccggtctacagctcccagcgtgagcgacgcagaa',
            'gacgggtgatttctgcatttccatctgaggtaccgggttcatctcactagggagtgccagacagtgggcg',
            'caggccagtgtgtgtgcgcaccgtgcgcgagccgaagcagggcgaggcattgcctcacctgggaagcgca',
            'aggggtcagggagttccctttccgagtcaaagaaaggggtgacggacgcacctggaaaatcgggtcactc',
        ])

        entry = next(iter(embl_file))
        self.assertEqual('gggaggaggagccaagatggccgaataggaacagctccggtctacagctcccagcgtgagcgacgcagaa'
            'gacgggtgatttctgcatttccatctgaggtaccgggttcatctcactagggagtgccagacagtgggcg'
            'caggccagtgtgtgtgcgcaccgtgcgcgagccgaagcagggcgaggcattgcctcacctgggaagcgca'
            'aggggtcagggagttccctttccgagtcaaagaaaggggtgacggacgcacctggaaaatcgggtcactc', entry.sequence)
