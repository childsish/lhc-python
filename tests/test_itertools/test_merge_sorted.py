import random
import unittest

from lhc.itertools.merge_sorted import merge_sorted


class TestMergeSorted(unittest.TestCase):
    def setUp(self):
        self.full_stream = 'JfVmmCQlaFdeQcKgAuPfxhLsunJgKCHoAmAbGaYekeLWHXmwCSGqmfeATWANGKWPDnAnbgusGWLlhKvwjxo'
        splits = [0] + sorted({random.randint(1, len(self.full_stream)) for i in range(4)}) + [len(self.full_stream)]
        self.lists = [self.full_stream[fr:to] for fr, to in zip(splits[:-1], splits[1:])]

    def test_merge_sorted(self):
        iterators = [iter(sorted(l)) for l in self.lists]
        it = merge_sorted(*iterators)

        self.assertEqual(sorted(self.full_stream), list(it))
