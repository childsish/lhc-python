import os
import pkgutil
import tempfile
import unittest

try:
    import pysam
    from lhc.io.fasta.index import IndexedFastaSet
except ImportError:
    pysam = None
    IndexedFastaSet = None


@unittest.skip('skip until test data included in package')
class TestIndexedFastaSet(unittest.TestCase):
    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.filename = 'tmp.fasta.gz'

        with open(os.path.join(self.dirname, self.filename), 'wb') as fileobj:
            fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.fasta.gz'))

        with open(os.path.join(self.dirname, self.filename + '.fai'), 'wb') as fileobj:
            fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.fasta.gz.fai'))

        with open(os.path.join(self.dirname, self.filename + '.gzi'), 'wb') as fileobj:
            fileobj.write(pkgutil.get_data('lhc.test', 'data/randome.fasta.gz.gzi'))

        self.index = pysam.FastaFile(os.path.join(self.dirname, self.filename))

    def test_get_item(self):
        parser = IndexedFastaSet(self.index)

        self.assertEqual('CGACAACACACTCCGGGTAAAACAATGATCGACAGGGAACCACCACATACCTCCTTCACCGAGTTGTTAGTGTACGCCTTTTTGTTGTGATGATTAAATG', parser['chr1'][100:200])
        self.assertEqual('CGACCTACAGGCTTCGTGTGCGAGCTAAACTTGAGGCCGCCGTCCAGCGATCATCGTGTGTCTAGCAGGAAGCTTCTGGTAACGAAGATCGTTAAGCAGG', parser['chr2'][100:200])

    def test_get_fetch(self):
        parser = IndexedFastaSet(self.index)

        self.assertEqual('C', parser.fetch('chr1', 100))
        self.assertEqual('C', parser.fetch('chr2', 100))

        self.assertEqual('CGACAACACACTCCGGGTAAAACAATGATCGACAGGGAACCACCACATACCTCCTTCACCGAGTTGTTAGTGTACGCCTTTTTGTTGTGATGATTAAATG', parser.fetch('chr1', 100, 200))
        self.assertEqual('CGACCTACAGGCTTCGTGTGCGAGCTAAACTTGAGGCCGCCGTCCAGCGATCATCGTGTGTCTAGCAGGAAGCTTCTGGTAACGAAGATCGTTAAGCAGG', parser.fetch('chr2', 100, 200))

    def tearDown(self):
        self.index.close()
        os.remove(os.path.join(self.dirname, self.filename))
        os.remove(os.path.join(self.dirname, self.filename + '.fai'))
        os.remove(os.path.join(self.dirname, self.filename + '.gzi'))
        os.rmdir(self.dirname)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
