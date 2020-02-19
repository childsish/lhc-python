import io
import unittest

from lhc.io.fasta.tools.wrap import split_chunk, wrap


class TestWrap(unittest.TestCase):
    def test_split_chunk(self):
        self.assertEqual(list(split_chunk('acgatgcatgcta\n>header\nacgatcgatcg\na\nc\ng\nt', 2)),
                         ['ac', 'ga', 'tg', 'ca', 'tg', 'ct', 'a', '>header', 'ac', 'ga', 'tc', 'ga', 'tc', 'ga', 'cg'])

        self.assertEqual(list(split_chunk('acgacgacg', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('acg\nacg\nacg', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('acg\nac\ngacg', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('acg\nacga\ncg', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('acg\nacg\nacg\n', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('acg\nacg\nacg\na', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('acg\nacg\nacg\nac', 3)), ['acg', 'acg', 'acg'])
        self.assertEqual(list(split_chunk('\nacg\nacg\nacg', 3)), ['acg', 'acg', 'acg'])

    def test_wrap(self):
        self.assertEqual(list(wrap(io.StringIO('aaaaaaacccccccgggggggttttttt'), width=3, chunk_size=7)),
                         ['aaa', 'aaa', 'acc', 'ccc', 'ccg', 'ggg', 'ggg', 'ttt', 'ttt', 't'])
        self.assertEqual(list(wrap(
            io.StringIO('actagtcgatgc\n>header header header header\natcg\natgctagagtcga\ngt'),
            width=3,
            chunk_size=7)
        ),
            ['act', 'agt', 'cga', 'tgc', '>header header header header', 'atc', 'gat', 'gct', 'aga', 'gtc', 'gag', 't'])
        self.assertEqual(list(wrap(
            io.StringIO('actagtcgatgc\n>header header header header\natcg\natgctagagtcga\ngt'),
            width=3,
            chunk_size=8)
        ),
            ['act', 'agt', 'cga', 'tgc', '>header header header header', 'atc', 'gat', 'gct', 'aga', 'gtc', 'gag', 't'])
