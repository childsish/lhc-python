import unittest

from lhc.entities.genomic_coordinate import GenomicInterval
from lhc.cli.loci import extend


class TestExtend(unittest.TestCase):
    def test_extend_5p(self):
        intervals = list(extend((
            GenomicInterval(100, 100, chromosome='chr1'), GenomicInterval(100, 100, chromosome='chr1')),
            five_prime=5))

        self.assertEqual(intervals, [GenomicInterval(95, 100, chromosome='chr1'), GenomicInterval(95, 100, chromosome='chr1')])

    def test_extend_3p(self):
        intervals = list(extend((
            GenomicInterval(100, 100, chromosome='chr1'), GenomicInterval(100, 100, chromosome='chr1')),
            three_prime=5))

        self.assertEqual(intervals, [GenomicInterval(100, 105, chromosome='chr1'), GenomicInterval(100, 105, chromosome='chr1')])

    def test_extend_5p_3p(self):
        intervals = list(extend((
            GenomicInterval(100, 100, chromosome='chr1'), GenomicInterval(100, 100, chromosome='chr1')),
            five_prime=5, three_prime=5))

        self.assertEqual(intervals, [GenomicInterval(95, 105, chromosome='chr1'), GenomicInterval(95, 105, chromosome='chr1')])
