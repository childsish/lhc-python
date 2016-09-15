import unittest

from lhc.io.gtf.iterator import GtfLineIterator, GtfEntryIterator


class TestGtfEntryIterator(unittest.TestCase):
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
            'chr1\t.\tCDS\t5100\t5900\t0\t+\t0\tgene_name "b";transcript_id "b.0"',
            'chr2\t.\tgene\t1000\t2000\t0\t-\t0\tgene_name "c"',
            'chr2\t.\ttranscript\t1000\t2000\t0\t-\t0\tgene_name "c";transcript_id "c.0"',
            'chr2\t.\tCDS\t1100\t1300\t0\t-\t0\tgene_name "c";transcript_id "c.0"',
            'chr2\t.\tCDS\t1330\t1600\t0\t-\t0\tgene_name "c";transcript_id "c.0"',
            'chr2\t.\tCDS\t1660\t1900\t0\t-\t0\tgene_name "c";transcript_id "c.0"'
        ]

    def test_parse_attributes(self):
        attr = GtfLineIterator.parse_attributes('gene_id "a"; transcript_id "a.0"; exon 1')

        self.assertEqual(attr['gene_id'], 'a')
        self.assertEqual(attr['transcript_id'], 'a.0')
        self.assertEqual(attr['exon'], 1)

    def test_parse_line(self):
        line = GtfLineIterator.parse_line('chr1\t.\tgene\t1000\t2000\t0\t+\t0\tgene_id "a"\n')

        self.assertEqual(line.chr, 'chr1')
        self.assertEqual(line.start, 999)
        self.assertEqual(line.stop, 2000)
        self.assertEqual(line.strand, '+')
        self.assertEqual(line.attr['gene_id'], 'a')

    def test_get_features(self):
        gene = GtfEntryIterator.get_features(self.lines[:8])[0]

        self.assertEqual('a', gene.name)
        self.assertEqual('a.1', gene.children[0].name)
        self.assertEqual('a.0', gene.children[1].name)
        exon = gene.children[1].children[-1]
        self.assertEqual((1659, 1900), (exon.start, exon.stop))

    def test_parse_gene_reverse_strand(self):
        gene = GtfEntryIterator.get_features(self.lines[-5:])[0]

        self.assertEqual('c', gene.name)
        self.assertEqual(0, gene.children[0].get_rel_pos(1899))
        self.assertEqual(711, gene.children[0].get_rel_pos(1100))

    def test_iter_gtf(self):
        it = GtfEntryIterator(iter(self.lines))
        
        gene = next(it)
        self.assertEqual('a', gene.name)
        self.assertEqual(2, len(gene.children))
        self.assertEqual('a.1', gene.children[0].name)
        self.assertEqual('a.0', gene.children[1].name)
        self.assertEqual(2, len(gene.children[0].children))
        self.assertEqual(3, len(gene.children[1].children))
        
        gene = next(it)
        self.assertEqual('b', gene.name)
        self.assertEqual(1, len(gene.children))
        self.assertEqual('b.0', gene.children[0].name)
        self.assertEqual(1, len(gene.children[0].children))

        gene = next(it)
        self.assertEqual('c', gene.name)
        self.assertEqual(1, len(gene.children))
        self.assertEqual('c.0', gene.children[0].name)
        self.assertEqual(3, len(gene.children[0].children))
        
        self.assertRaises(StopIteration, it.__next__)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
