import random
import unittest

from itertools import chain
from lhc.itertools.merge_sorted import merge_sorted


class TestMergeSorted(unittest.TestCase):
    def setUp(self):
        self.full_stream = 'JfVmmCQlaFdeQcKgAuPfxhLsunJgKCHoAmAbGaYekeLWHXmwCSGqmfeATWANGKWPDnAnbgusGWLlhKvwjxo'
        splits = [0] + sorted({random.randint(1, len(self.full_stream)) for i in range(4)}) + [len(self.full_stream)]
        self.lists = [self.full_stream[fr:to] for fr, to in zip(splits[:-1], splits[1:])]

    def test_merge_sorted(self):
        iterators = [iter(sorted(l)) for l in self.lists]
        it = merge_sorted(*iterators)

        self.assertEqual(sorted(self.full_stream), list(chain.from_iterable(chain.from_iterable(it))))

    def test_merge_sorted_reverse(self):
        key = lambda x: -ord(x)
        iterators = [iter(sorted(l, key=key)) for l in self.lists]
        it = merge_sorted(*iterators, key=key)

        self.assertEqual(sorted(self.full_stream, key=key), list(chain.from_iterable(chain.from_iterable(it))))

    def test_merge_sorted_not_flattened(self):
        iterators = [iter(sorted(l)) for l in self.lists]
        it = merge_sorted(*iterators)

        self.assertEqual(['A', 'A', 'A', 'A', 'A', 'A'], list(chain.from_iterable(next(it))))

    def test_merge_sorted_flattened(self):
        iterators = [iter(sorted(l)) for l in self.lists]
        it = merge_sorted(*iterators, flatten=True)


        self.assertEqual(['A', 'A', 'A', 'A', 'A', 'A'], next(it))