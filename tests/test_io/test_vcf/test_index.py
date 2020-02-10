import os
import pkgutil
import tempfile
import unittest


try:
    import pysam

    from lhc.io.vcf.index import IndexedVcfFile


    @unittest.skip('skip until test data included in package')
    class TestIndexedVcfFile(unittest.TestCase):
        def setUp(self):
            self.dirname = tempfile.mkdtemp()
            self.filename = 'tmp.vcf.gz'

            with open(os.path.join(self.dirname, self.filename), 'wb') as fileobj:
                fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.vcf.gz'))

            with open(os.path.join(self.dirname, self.filename + '.tbi'), 'wb') as fileobj:
                fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.vcf.gz.tbi'))

            self.index = pysam.TabixFile(os.path.join(self.dirname, self.filename))

        def test_fetch(self):
            parser = IndexedVcfFile(os.path.join(self.dirname, self.filename), self.index)

            variants = parser.fetch('chr1', 99)
            self.assertEqual(1, len(variants))
            self.assertEqual('chr1', variants[0].chr)
            self.assertEqual(99, variants[0].pos)
            self.assertEqual('.', variants[0].id)
            self.assertEqual('A', variants[0].ref)
            self.assertEqual('C', variants[0].alt)
            self.assertAlmostEqual(100, variants[0].qual)
            self.assertEqual('PASS', variants[0].filter)
            self.assertEqual({'RO': '50', 'AO': '50', 'AF': '0.5'}, variants[0].info)
            self.assertEqual({}, variants[0].samples)

            variants = parser.fetch('chr2', 100, 1000)
            self.assertEqual(15, len(variants))

        def tearDown(self):
            self.index.close()
            os.remove(os.path.join(self.dirname, self.filename))
            os.remove(os.path.join(self.dirname, self.filename + '.tbi'))
            os.rmdir(self.dirname)


    if __name__ == '__main__':
        import sys
        sys.exit(unittest.main())
except ImportError:
    pass