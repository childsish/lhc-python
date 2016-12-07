import unittest

from io import StringIO
from lhc.io.vcf import VcfIterator, VcfMerger
from lhc.order import natural_key


class TestMerger(unittest.TestCase):
    def setUp(self):
        self.vcf1 = VcfIterator(StringIO('''##version=VCF2.0
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
chr1\t101\ta0\ta\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr1\t201\ta1\tg\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr10\t101\ta2\tt\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr10\t201\ta2\tt\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr20\t101\ta4\tc\tcAAG\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr20\t201\ta4\tc\tcAAG\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0'''))
        self.vcf2 = VcfIterator(StringIO('''##version=VCF2.0
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts2
chr1\t101\ta0\ta\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr1\t201\ta1\tg\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr2\t101\ta3\ttACG\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr2\t201\ta3\ttACG\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr20\t101\ta4\tc\tcAAG\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0
chr20\t201\ta4\tc\tcAAG\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0'''))

    def test_merge_lexographical_order(self):
        merger = iter(VcfMerger([self.vcf1, self.vcf2]))

        variant = next(merger)
        self.assertEqual(('chr1', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr1', 200), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr10', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr10', 200), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr2', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr2', 200), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr20', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr20', 200), (variant.chromosome, variant.position))

    def test_merge_natural_order(self):
        merger = iter(VcfMerger([self.vcf1, self.vcf2], key=variant_key))

        variant = next(merger)
        self.assertEqual(('chr1', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr1', 200), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr2', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr2', 200), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr10', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr10', 200), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr20', 100), (variant.chromosome, variant.position))
        variant = next(merger)
        self.assertEqual(('chr20', 200), (variant.chromosome, variant.position))


def variant_key(variant):
    return (tuple(natural_key(variant.chromosome)), variant.position)


if __name__ == '__main__':
    unittest.main()
