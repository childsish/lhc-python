import unittest

from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.binf.loci import filter


class TestFilter(unittest.TestCase):
    def test_filter_chromosome(self):
        intervals = list(filter((
            GenomicInterval(0, 100, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1', strand='-'),
            GenomicInterval(0, 100, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2', strand='-')
        ), 'chromosome == "chr1"'))

        self.assertEqual(intervals, [
            GenomicInterval(0, 100, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1', strand='-')])

    def test_filter_position(self):
        intervals = list(filter((
            GenomicInterval(0, 100, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1', strand='-'),
            GenomicInterval(0, 100, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2', strand='-')
        ), 'start < 100 and 100 < stop'))

        self.assertEqual(intervals, [
            GenomicInterval(50, 150, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1', strand='-'),
            GenomicInterval(50, 150, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2', strand='-')])

    def test_filter_strand(self):
        intervals = list(filter((
            GenomicInterval(0, 100, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1'),
            GenomicInterval(50, 150, chromosome='chr1', strand='-'),
            GenomicInterval(0, 100, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2'),
            GenomicInterval(50, 150, chromosome='chr2', strand='-')
        ),
            'strand == "-"'
        ))

        self.assertEqual(intervals, [
            GenomicInterval(50, 150, chromosome='chr1', strand='-'),
            GenomicInterval(50, 150, chromosome='chr2', strand='-')])
