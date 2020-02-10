import os
import pkgutil
import tempfile
import unittest

from lhc.io.gff.index import IndexedGffFile

try:
    import pysam
except ImportError:
    pysam = None


@unittest.skip('skip until test data included in package')
class TestIndexedVcfFile(unittest.TestCase):
    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.filename = 'tmp.gff.gz'

        with open(os.path.join(self.dirname, self.filename), 'wb') as fileobj:
            fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.gff.gz'))

        with open(os.path.join(self.dirname, self.filename + '.tbi'), 'wb') as fileobj:
            fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.gff.gz.tbi'))

        self.index = pysam.TabixFile(os.path.join(self.dirname, self.filename))

    def test_fetch(self):
        parser = IndexedGffFile(self.index)

        genomic_features = parser.fetch('chr1', 99)
        self.assertEqual(1, len(genomic_features))
        self.assertEqual('chr1', genomic_features[0].chr)
        self.assertEqual(50, genomic_features[0].start)
        self.assertEqual(211, genomic_features[0].stop)
        self.assertEqual({'ID': 'gene0'}, genomic_features[0].data)
        self.assertEqual('gene0', genomic_features[0].name)
        self.assertEqual('+', genomic_features[0].strand)
        self.assertEqual('gene', genomic_features[0].type)

        genomic_features = parser.fetch('chr2', 100, 1000)
        self.assertEqual(2, len(genomic_features))

    def tearDown(self):
        self.index.close()
        os.remove(os.path.join(self.dirname, self.filename))
        os.remove(os.path.join(self.dirname, self.filename + '.tbi'))
        os.rmdir(self.dirname)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
