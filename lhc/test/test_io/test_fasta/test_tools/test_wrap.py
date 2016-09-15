import unittest
from io import StringIO

from lhc.io.fasta.tools.wrap import wrap_input


class TestWrap(unittest.TestCase):
    def setUp(self):
        self.in_fhndl = StringIO('>chr1\naaccggtt\naaccggtt\naa\n>chr2\naaacccgggtttt\naaacccgggtttt\na')

    def test_wrap_input(self):
        it = wrap_input(self.in_fhndl, 20, 4)

        self.assertEqual('', next(it))
        self.assertEqual('>chr1', next(it))
        self.assertEqual('aacc', next(it))
        self.assertEqual('ggtt', next(it))
        self.assertEqual('aacc', next(it))
        self.assertEqual('ggtt', next(it))
        self.assertEqual('aa', next(it))
        self.assertEqual('>chr2', next(it))
        self.assertEqual('aaac', next(it))
        self.assertEqual('ccgg', next(it))
        self.assertEqual('gttt', next(it))
        self.assertEqual('taaa', next(it))
        self.assertEqual('cccg', next(it))
        self.assertEqual('ggtt', next(it))
        self.assertEqual('tta', next(it))
