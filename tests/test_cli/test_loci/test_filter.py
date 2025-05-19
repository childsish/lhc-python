import unittest

from lhc.entities.locus import Locus
from lhc.cli.loci.filter import filter


class TestFilter(unittest.TestCase):
    def test_filter_chromosome(self):
        intervals = list(filter((
            Locus(0, 100, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1', strand='-'),
            Locus(0, 100, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2', strand='-')
        ), 'chromosome == "chr1"'))

        self.assertEqual(intervals, [
            Locus(0, 100, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1', strand='-')])

    def test_filter_position(self):
        intervals = list(filter((
            Locus(0, 100, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1', strand='-'),
            Locus(0, 100, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2', strand='-')
        ), 'start < 100 and 100 < end'))

        self.assertEqual(intervals, [
            Locus(50, 150, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1', strand='-'),
            Locus(50, 150, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2', strand='-')])

    def test_filter_strand(self):
        intervals = list(filter((
            Locus(0, 100, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1'),
            Locus(50, 150, chromosome='chr1', strand='-'),
            Locus(0, 100, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2'),
            Locus(50, 150, chromosome='chr2', strand='-')
        ), 'strand == "-"'))

        self.assertEqual(intervals, [
            Locus(50, 150, chromosome='chr1', strand='-'),
            Locus(50, 150, chromosome='chr2', strand='-')])
