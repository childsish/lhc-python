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

        self.assertEquals(attr['gene_id'], 'a')
        self.assertEquals(attr['transcript_id'], 'a.0')
        self.assertEquals(attr['exon'], 1)

    def test_parse_line(self):
        line = GtfLineIterator.parse_line('chr1\t.\tgene\t1000\t2000\t0\t+\t0\tgene_id "a"\n')

        self.assertEquals(line.chr, 'chr1')
        self.assertEquals(line.start, 999)
        self.assertEquals(line.stop, 2000)
        self.assertEquals(line.strand, '+')
        self.assertEquals(line.attr['gene_id'], 'a')

    def test_get_features(self):
        gene = GtfEntryIterator.get_features(self.lines[:8])[0]

        self.assertEquals('a', gene.name)
        self.assertEquals('a.1', gene.children[0].name)
        self.assertEquals('a.0', gene.children[1].name)
        exon = gene.children[1].children[-1]
        self.assertEquals((1659, 1900), (exon.start, exon.stop))

    def test_parse_gene_reverse_strand(self):
        gene = GtfEntryIterator.get_features(self.lines[-5:])[0]

        self.assertEquals('c', gene.name)
        self.assertEquals(0, gene.children[0].get_rel_pos(1899))
        self.assertEquals(711, gene.children[0].get_rel_pos(1100))

    def test_iter_gtf(self):
        it = GtfEntryIterator(iter(self.lines))
        
        gene = it.next()
        self.assertEquals('a', gene.name)
        self.assertEquals(2, len(gene.children))
        self.assertEquals('a.1', gene.children[0].name)
        self.assertEquals('a.0', gene.children[1].name)
        self.assertEquals(2, len(gene.children[0].children))
        self.assertEquals(3, len(gene.children[1].children))
        
        gene = it.next()
        self.assertEquals('b', gene.name)
        self.assertEquals(1, len(gene.children))
        self.assertEquals('b.0', gene.children[0].name)
        self.assertEquals(1, len(gene.children[0].children))

        gene = it.next()
        self.assertEquals('c', gene.name)
        self.assertEquals(1, len(gene.children))
        self.assertEquals('c.0', gene.children[0].name)
        self.assertEquals(3, len(gene.children[0].children))
        
        self.assertRaises(StopIteration, it.next)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
