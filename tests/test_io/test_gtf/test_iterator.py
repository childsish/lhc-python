import unittest

from lhc.binf.genomic_coordinate import GenomicPosition
from lhc.io.gtf import GtfConverter


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
        attr = GtfConverter.parse_attributes('gene_id "a"; transcript_id "a.0"; exon 1')

        self.assertEqual(attr['gene_id'], 'a')
        self.assertEqual(attr['transcript_id'], 'a.0')
        self.assertEqual(attr['exon'], 1)

    @unittest.skip("skip until fixed")
    def test_parse_line(self):
        converter = GtfConverter()
        line = converter.parse('chr1\t.\tgene\t1000\t2000\t0\t+\t0\tgene_id "a"\n')

        self.assertEqual(line.chromosome, 'chr1')
        self.assertEqual(line.start, GenomicPosition('chr1', 999))
        self.assertEqual(line.stop, GenomicPosition('chr1', 2000))
        self.assertEqual(line.strand, '+')
        self.assertEqual(line.data['attr']['gene_id'], 'a')

    def test_iter_gtf(self):
        it = iter(GtfConverter(iter(self.lines)))
        
        gene = next(it)
        self.assertEqual('a', gene.data['gene_name'])
        
        gene = next(it)
        self.assertEqual('a', gene.data['gene_name'])

        gene = next(it)
        self.assertEqual('a', gene.data['gene_name'])


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
