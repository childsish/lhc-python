import unittest

from lhc.io.fasta_.inorder_access_set import FastaInOrderAccessSet


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.lines = [
            '>a\n',
            'aaaaacccccgggggttttt\n',
            'AAAAACCCCCGGGGGTTTTT\n',
            'aaaaacccccgggggttttt\n',
            'AAAAACCCCCGGGGGTTTTT\n',
            '>b\n',
            'aaaaacccccgggggttttt\n',
            'AAAAACCCCCGGGGGTTTTT\n',
            'aaaaacccccgggggttttt\n',
            'AAAAACCCCCGGGGGTTTTT\n',
            '>c\n',
            'aaaaacccccgggggttttt\n',
            '>d\n',
            'aaaaacccccgggggttttt\n',
            'AAAAACCCCCGGGGGTTTTT\n'
        ]

    def test_fetch(self):
        set_ = FastaInOrderAccessSet(iter(self.lines))

        self.assertEqual('aaaaa', set_.fetch('a', 0, 5))
        self.assertEqual('cccccgggggttttt', set_.fetch('a', 5, 20))
        self.assertEqual('ggggg', set_.fetch('a', 10, 15))
        self.assertEqual('tttttAAAAA', set_.fetch('a', 15, 25))
        self.assertEqual('TTTTTaaaaacccccgggggtttttAAAAA', set_.fetch('a', 35, 65))
        self.assertEqual('aaaaa', set_.fetch('b', 0, 5))
        self.assertEqual('TTTTTaaaaacccccgggggtttttAAAAA', set_.fetch('b', 35, 65))
        self.assertEqual('CCCCCGGGGG', set_.fetch('d', 25, 35))


if __name__ == '__main__':
    unittest.main()
