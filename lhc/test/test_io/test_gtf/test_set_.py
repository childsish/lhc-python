import unittest

from lhc.io.gtf.iterator import GtfIterator, GtfLineIterator
from lhc.io.gtf.set_ import GtfSet


class TestGtfSet(unittest.TestCase):
    def setUp(self):
        self.lines = [
            'chr1\t.\tgene\t1000\t2000\t0\t+\t0\tgene_name "a"',
            'chr1\t.\ttranscript\t1000\t2000\t0\t+\t0\tgene_name "a";transcript_id "a.0"',
            'chr1\t.\tCDS\t1100\t1300\t0\t+\t0\tgene_name "a";transcript_id "a.0"',
            'chr1\t.\tCDS\t1330\t1600\t0\t+\t0\tgene_name "a";transcript_id "a.0"',
            'chr1\t.\tCDS\t1660\t1900\t0\t+\t0\tgene_name "a";transcript_id "a.0"',
            'chr1\t.\ttranscript\t1000\t2000\t0\t+\t0\tgene_name "a";transcript_id "a.1"',
            'chr1\t.\tCDS\t1100\t1300\t0\t+\t0\tgene_name "a";transcript_id "a.1"',
            'chr1\t.\tCDS\t1660\t1900\t0\t+\t0\tgene_name "a";transcript_id "a.1"',
            'chr1\t.\tgene\t5000\t6000\t0\t+\t0\tgene_name "b"',
            'chr1\t.\ttranscript\t5000\t6000\t0\t+\t0\tgene_name "b";transcript_id "b.0"',
            'chr1\t.\tCDS\t5100\t5900\t0\t+\t0\tgene_name "b";transcript_id "b.0"'
        ]

    def test_getItemByKey(self):
        parser = GtfSet(GtfIterator(GtfLineIterator(iter(self.lines))))

        gene = parser['a']
        self.assertEqual(gene.data['name'], 'a')
        self.assertEqual(len(gene.children), 2)
        self.assertEqual(gene.children[0].data['name'], 'a.0')
        self.assertEqual(len(gene.children[0].children), 3)
        self.assertEqual(gene.children[1].data['name'], 'a.1')
        self.assertEqual(len(gene.children[1].children), 2)

        gene = parser['b']
        self.assertEqual(gene.data['name'], 'b')
        self.assertEqual(len(gene.children), 1)
        self.assertEqual(gene.children[0].data['name'], 'b.0')
        self.assertEqual(len(gene.children[0].children), 1)

    def test_getItemInterval(self):
        parser = GtfSet(GtfIterator(GtfLineIterator(iter(self.lines))))

        genes = parser.fetch('chr1', 500, 1500)
        self.assertEqual(len(genes), 1)
        self.assertEqual(genes[0].data['name'], 'a')

        genes = parser.fetch('chr1', 1500, 5500)
        self.assertEqual(len(genes), 2)
        self.assertEqual(set(gene.data['name'] for gene in genes), set('ab'))

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
