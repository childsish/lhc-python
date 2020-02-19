import unittest

from lhc.binf.genomic_coordinate import GenomicInterval
from lhc.binf.loci import view


class TestView(unittest.TestCase):
    def test_view(self):
        intervals = list(view((GenomicInterval(0, 100), GenomicInterval(50, 150))))

        self.assertEqual(intervals, [GenomicInterval(0, 100), GenomicInterval(50, 150)])
