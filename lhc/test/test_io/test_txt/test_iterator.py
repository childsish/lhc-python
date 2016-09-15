import os
import tempfile
import unittest

from lhc.io.txt import Iterator


@unittest.skip('obsolete and will be removed')
class TestIterator(unittest.TestCase):
    def setUp(self):
        self.lines = ['#version=1.0\n',
                      '#date=010101\n',
                      'chr\tstart\tstop\tgene\n',
                      'chr1\t10\t20\ta\n',
                      'chr1\t30\t60\tb\n',
                      'chr1\t100\t110\tc\n',
                      'chr2\t15\t30\td\n',
                      'chr2\t40\t50\te\n',
                      'chr3\t10\t110\tf\n']

    def test_iterator(self):
        lines = list(Iterator(iter(self.lines), has_header=True))

        self.assertEqual(9, len(lines))
        self.assertEqual('comment', lines[0].type)
        self.assertEqual(self.comment[0], lines[0].value)
        self.assertEqual('comment', lines[1].type)
        self.assertEqual(self.comment[1], lines[1].value)
        self.assertEqual('header', lines[2].type)
        self.assertEqual(self.header, lines[2].value)
        self.assertEqual('line', lines[3].type)
        self.assertEqual(self.data[0], lines[3].value)
        self.assertEqual('line', lines[4].type)
        self.assertEqual(self.data[1], lines[4].value)
        self.assertEqual('line', lines[5].type)
        self.assertEqual(self.data[2], lines[5].value)
        self.assertEqual('line', lines[6].type)
        self.assertEqual(self.data[3], lines[6].value)
        self.assertEqual('line', lines[7].type)
        self.assertEqual(self.data[4], lines[7].value)
        self.assertEqual('line', lines[8].type)
        self.assertEqual(self.data[5], lines[8].value)


if __name__ == '__main__':
    unittest.main()
