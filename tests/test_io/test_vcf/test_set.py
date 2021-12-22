import os
import tempfile
import unittest

from lhc.io.variant import VariantFile
from lhc.io.vcf.set_ import VcfSet


class TestSet(unittest.TestCase):
    def setUp(self):
        fhndl, self.fname = tempfile.mkstemp()
        os.write(fhndl, b'##VCF=2.0\n'
                        b'#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\n'
                        b'chr1\t101\ta0\ta\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'
                        b'chr1\t201\ta1\tg\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'
                        b'chr1\t301\ta2\tt\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'
                        b'chr1\t401\ta3\ttACG\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'
                        b'chr1\t501\ta4\tc\tcAAG\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n')
        os.close(fhndl)

    @unittest.skip("skip until fixed")
    def test_getItemByPos(self):
        with open(self.fname) as fileobj:
            parser = VcfSet(VariantFile(fileobj))

            var = parser.fetch('chr1', 100)
            self.assertEqual(len(var), 1)
            var = var[0]
            self.assertEqual('chr1', var.chromosome)
            self.assertEqual(100, var.position)
            self.assertEqual('a0', var.data['id'])
            self.assertEqual('a', var.data['ref'])
            self.assertEqual(['t'], var.data['alt'])
            self.assertEqual(40, var.data['qual'])
            self.assertEqual({'PASS'}, var.data['filter'])
            self.assertEqual({'GT': '5'}, var.data['info'])

    @unittest.skip("skip until fixed")
    def test_getItemByInterval(self):
        with open(self.fname) as fileobj:
            parser = VcfSet(VariantFile(fileobj))

            vars = parser.fetch('chr1', 50, 150)
            self.assertEqual(len(vars), 1)
            self.assertEqual(vars[0].data['id'], 'a0')

            vars = parser.fetch('chr1', 50, 250)
            self.assertEqual(len(vars), 2)
            self.assertEqual(set(var.data['id'] for var in vars), {'a0', 'a1'})


if __name__ == '__main__':
    unittest.main()
