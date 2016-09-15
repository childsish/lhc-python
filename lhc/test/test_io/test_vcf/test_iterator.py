__author__ = 'Liam Childs'

import os
import tempfile
import unittest

from lhc.io.vcf.iterator import VcfEntryIterator

class TestIterator(unittest.TestCase):
    
    def setUp(self):
        fhndl, self.fname = tempfile.mkstemp()
        os.write(fhndl, '##VCF=2.0\n'\
            '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\n'\
            'chr1\t101\ta0\ta\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'\
            'chr1\t201\ta1\tg\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'\
            'chr1\t301\ta2\tt\tc\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'\
            'chr1\t401\ta3\ttACG\tt\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n'\
            'chr1\t501\ta4\tc\tcAAG\t40\tPASS\tGT=5\tGT:GQ\t0/1:100.0\n')
        os.close(fhndl)
    
    def test_iterEntries(self):
        it = VcfEntryIterator(open(self.fname))
        
        var = next(it)
        self.assertEqual('chr1', var.chr)
        self.assertEqual(100, var.pos)
        self.assertEqual('a0', var.id)
        self.assertEqual('a', var.ref)
        self.assertEqual('t', var.alt)
        self.assertEqual(40, var.qual)
        self.assertEqual('PASS', var.filter)
        self.assertEqual({'GT': '5'}, var.info)
        self.assertEqual({'s1': {'GT': '0/1', 'GQ': '100.0'}}, var.samples)
        self.assertEqual('a1', it.next().id)
        self.assertEqual('a2', it.next().id)
        self.assertEqual('a3', it.next().id)
        self.assertEqual('a4', it.next().id)
        self.assertRaises(StopIteration, it.__next__)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
