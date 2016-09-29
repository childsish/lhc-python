import os
import tempfile
import unittest

from lhc.io.vcf.iterator import VcfIterator


class TestIterator(unittest.TestCase):
    
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
    
    def test_iterEntries(self):
        with open(self.fname, encoding='utf-8') as fileobj:
            it = VcfIterator(fileobj)

            var = next(it)
            self.assertEqual('chr1', var.pos.chromosome)
            self.assertEqual(100, var.pos.position)
            self.assertEqual('a0', var.id)
            self.assertEqual('a', var.ref)
            self.assertEqual(['t'], var.alt)
            self.assertEqual(40, var.qual)
            self.assertEqual({'PASS'}, var.filter)
            self.assertEqual({'GT': '5'}, var.info)
            self.assertEqual({'s1': {'GT': '0/1', 'GQ': '100.0'}}, var.samples)
            self.assertEqual('a1', next(it).id)
            self.assertEqual('a2', next(it).id)
            self.assertEqual('a3', next(it).id)
            self.assertEqual('a4', next(it).id)
            self.assertRaises(StopIteration, next, it)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
